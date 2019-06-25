#  Modified by Qentinel 2018

#  Copyright 2008-2015 Nokia Networks
#  Copyright 2016-     Robot Framework Foundation
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

from robot.errors import ExecutionFailed, DataError, PassExecution
from robot.model import SuiteVisitor
from robot.result import TestSuite, Result
from robot.utils import get_timestamp, is_list_like, NormalizedDict, unic
from robot.variables import VariableScopes

from .context import EXECUTION_CONTEXTS
from .steprunner import StepRunner
from .namespace import IMPORTER, Namespace
from .status import SuiteStatus, TestStatus
from .timeouts import TestTimeout

from robot.libraries.BuiltIn import BuiltIn
from pathlib import Path
import xml.etree.ElementTree as ET

class Flow(object):
    """ Custom class for flow control """
    def __init__(self, graph, initial=None):
        self.verbose = False
        self.graph = graph
        print(self.graph)
        if initial:
            self.initial = initial
        else:
            self.initial = self.parse_initial()
        self._state = None 
        self.running = False

    def parse_initial(self):
        for s in self.graph:
            found = False
            if self.verbose:
                print(s)
            for i in self.graph:
                if self.graph[i]["target"]:
                    if s in self.graph[i]["target"][0]:
                        found = True
            if not found:
                if self.verbose:
                    print("found initial: {}".format(s))
                return s
        return None
                        
    def state(self):
        if self.verbose:
            print("state: {}".format(self._state))
        return self._state

    def next(self, input=None):
        if not self.running:
            self._state = self.initial
            self.running = True
            return self._state
        if not self._state:
            # has reached the end
            return None
        new = self.graph[self._state]["target"]
        if not new:
            # last state, no target
            self._state = None
            return None
        # tuple assumed
        for n, cond in new:
            if self.verbose:
                print("n: {}, cond: {}".format(n, cond))
            if cond == None:
                self._state = n
                return n
            # check validity before eval
            self._validate_cond(cond)
            if input == cond:
                self._state = n
                return n


    def _validate_cond(self, cond):
        """ Validate allowed strings to be passed for evaluation """
        if cond.lower() not in ["true", "false"]:
            raise NotImplementedError("only true or false are accepted as conditions")

def parse_graph(filename, verbose=False):
    tree = ET.parse(str(filename))
    root = tree.getroot()

    id2node = {}
    nodes = {}
    for e in root.iter('{http://graphml.graphdrawing.org/xmlns}node'):
        id = e.attrib["id"]
        for label in e.iter('{http://www.yworks.com/xml/graphml}GenericNode'):
            type = label.attrib["configuration"]
        for label in e.iter('{http://www.yworks.com/xml/graphml}NodeLabel'):
            label = label.text
        nodes[label] = {}
        nodes[label]["id"] = id
        nodes[label]["type"] = type
        nodes[label]["target"] = None
        id2node[id] = label

    if verbose:
        print(nodes)
        print(id2node)

    for e in root.iter('{http://graphml.graphdrawing.org/xmlns}edge'):
        source = id2node[e.attrib["source"]]
        target = id2node[e.attrib["target"]]
        if verbose:
            print(source + ":" + target)
        target_label = None
        for label in e.iter('{http://www.yworks.com/xml/graphml}EdgeLabel'):
            target_label = label.text
        if not nodes[source]["target"]:
            nodes[source]["target"] = [(target, target_label)]
        else:
            # multiple targets
            nodes[source]["target"].append((target, target_label))
    return nodes


# Some 'extract method' love needed here. Perhaps even 'extract class'.

class Runner(SuiteVisitor):

    def __init__(self, output, settings):
        self.verbose = False
        self.result = None
        self._output = output
        self._settings = settings
        self._variables = VariableScopes(settings)
        self._suite = None
        self._suite_status = None
        self._executed_tests = None

    @property
    def _context(self):
        return EXECUTION_CONTEXTS.current

    def visit_suite(self, suite):
        """ Overwritten version.
        """
        if self.verbose:
            print("visit_suite: {}, {}, tests: {}".format(suite, type(suite), suite.tests))

        if self.start_suite(suite) is not False:            
            suite.keywords.visit(self)
            suite.suites.visit(self)

            print("Script file: {}".format(suite.source))
            graph_file = suite.source.split(".")[0] + ".graphml"
            print("GraphML file: {}".format(graph_file))
            graph = Path(graph_file)
            if not graph.exists():
                raise DataError("File not found: {}".format(graph_file))
            self.parsed_graph = parse_graph(graph_file, self.verbose)
            self.flow = Flow(self.parsed_graph)

            # Special logic to allow controlling the next executed test.
            self.tests = suite.tests
            
            output = BuiltIn().get_variable_value("${OUTPUT}")
            test = self.str2test(self.flow.next(output))
            if self.verbose:
                print("Next test: {}, {}".format(test, self.tests))
            while test:
                if self.verbose:
                    print("runner.py: Starting {}".format(test.name))
                test.visit(self)
                output = BuiltIn().get_variable_value("${OUTPUT}")
                if self.verbose:
                    print("runner.py: Completed {}, output {}".format(test.name, output))
                test = self.str2test(self.flow.next(output))

            self.end_suite(suite)

    def str2test(self, testname):
        """ Return test case object """
        for t in self.tests:
            if testname == t.name:
                return t
        return None
        
    def start_suite(self, suite):
        self._output.library_listeners.new_suite_scope()
        result = TestSuite(source=suite.source,
                           name=suite.name,
                           doc=suite.doc,
                           metadata=suite.metadata,
                           starttime=get_timestamp())
        if not self.result:
            result.set_criticality(self._settings.critical_tags,
                                   self._settings.non_critical_tags)
            self.result = Result(root_suite=result)
            self.result.configure(status_rc=self._settings.status_rc,
                                  stat_config=self._settings.statistics_config)
        else:
            self._suite.suites.append(result)
        self._suite = result
        self._suite_status = SuiteStatus(self._suite_status,
                                         self._settings.exit_on_failure,
                                         self._settings.exit_on_error,
                                         self._settings.skip_teardown_on_exit)
        ns = Namespace(self._variables, result, suite.resource)
        ns.start_suite()
        ns.variables.set_from_variable_table(suite.resource.variables)
        EXECUTION_CONTEXTS.start_suite(result, ns, self._output,
                                       self._settings.dry_run)
        self._context.set_suite_variables(result)
        if not self._suite_status.failures:
            ns.handle_imports()
            ns.variables.resolve_delayed()
        result.doc = self._resolve_setting(result.doc)
        result.metadata = [(self._resolve_setting(n), self._resolve_setting(v))
                           for n, v in result.metadata.items()]
        self._context.set_suite_variables(result)
        self._output.start_suite(ModelCombiner(suite, result,
                                               tests=suite.tests,
                                               suites=suite.suites,
                                               test_count=suite.test_count))
        self._output.register_error_listener(self._suite_status.error_occurred)
        self._run_setup(suite.keywords.setup, self._suite_status)
        self._executed_tests = NormalizedDict(ignore='_')

    def _resolve_setting(self, value):
        if is_list_like(value):
            return self._variables.replace_list(value, ignore_errors=True)
        return self._variables.replace_string(value, ignore_errors=True)

    def end_suite(self, suite):
        self._suite.message = self._suite_status.message
        self._context.report_suite_status(self._suite.status,
                                          self._suite.full_message)
        with self._context.suite_teardown():
            failure = self._run_teardown(suite.keywords.teardown, self._suite_status)
            if failure:
                self._suite.suite_teardown_failed(unic(failure))
                if self._suite.statistics.critical.failed:
                    self._suite_status.critical_failure_occurred()
        self._suite.endtime = get_timestamp()
        self._suite.message = self._suite_status.message
        self._context.end_suite(ModelCombiner(suite, self._suite))
        self._suite = self._suite.parent
        self._suite_status = self._suite_status.parent
        self._output.library_listeners.discard_suite_scope()
        if not suite.parent:
            IMPORTER.close_global_library_listeners()

    def visit_test(self, test):
        if test.name in self._executed_tests:
            self._output.warn("Multiple test cases with name '%s' executed in "
                              "test suite '%s'." % (test.name, self._suite.longname))
        self._executed_tests[test.name] = True
        result = self._suite.tests.create(name=test.name,
                                          doc=self._resolve_setting(test.doc),
                                          tags=self._resolve_setting(test.tags),
                                          starttime=get_timestamp(),
                                          timeout=self._get_timeout(test))
        self._context.start_test(result)
        self._output.start_test(ModelCombiner(test, result))
        status = TestStatus(self._suite_status, result.critical)
        if not status.failures and not test.name:
            status.test_failed('Test case name cannot be empty.')
        if not status.failures and not test.keywords.normal:
            status.test_failed('Test case contains no keywords.')
        if status.exit:
            self._add_exit_combine()
            result.tags.add('robot-exit')
        self._run_setup(test.keywords.setup, status, result)
        try:
            if not status.failures:
                StepRunner(self._context,
                           test.template).run_steps(test.keywords.normal)
            else:
                status.test_failed(status.message)
        except PassExecution as exception:
            err = exception.earlier_failures
            if err:
                status.test_failed(err)
            else:
                result.message = exception.message
        except ExecutionFailed as err:
            status.test_failed(err)
        result.status = status.status
        result.message = status.message or result.message
        if status.teardown_allowed:
            with self._context.test_teardown(result):
                failure = self._run_teardown(test.keywords.teardown, status,
                                             result)
                if failure and result.critical:
                    status.critical_failure_occurred()
        if not status.failures and result.timeout and result.timeout.timed_out():
            status.test_failed(result.timeout.get_message())
            result.message = status.message
        result.status = status.status
        result.endtime = get_timestamp()
        self._output.end_test(ModelCombiner(test, result))
        self._context.end_test(result)

    def _add_exit_combine(self):
        exit_combine = ('NOT robot-exit', '')
        if exit_combine not in self._settings['TagStatCombine']:
            self._settings['TagStatCombine'].append(exit_combine)

    def _get_timeout(self, test):
        if not test.timeout:
            return None
        return TestTimeout(test.timeout.value, test.timeout.message,
                           self._variables)

    def _run_setup(self, setup, status, result=None):
        if not status.failures:
            exception = self._run_setup_or_teardown(setup)
            status.setup_executed(exception)
            if result and isinstance(exception, PassExecution):
                result.message = exception.message

    def _run_teardown(self, teardown, status, result=None):
        if status.teardown_allowed:
            exception = self._run_setup_or_teardown(teardown)
            status.teardown_executed(exception)
            failed = not isinstance(exception, PassExecution)
            if result and exception:
                result.message = status.message if failed else exception.message
            return exception if failed else None

    def _run_setup_or_teardown(self, data):
        if not data:
            return None
        try:
            name = self._variables.replace_string(data.name)
        except DataError as err:
            if self._settings.dry_run:
                return None
            return err
        if name.upper() in ('', 'NONE'):
            return None
        try:
            StepRunner(self._context).run_step(data, name=name)
        except ExecutionFailed as err:
            return err


class ModelCombiner(object):

    def __init__(self, data, result, **priority):
        self.data = data
        self.result = result
        self.priority = priority

    def __getattr__(self, name):
        if name in self.priority:
            return self.priority[name]
        if hasattr(self.result, name):
            return getattr(self.result, name)
        if hasattr(self.data, name):
            return getattr(self.data, name)
        raise AttributeError(name)
