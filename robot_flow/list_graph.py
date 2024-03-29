#
#  Copyright 2019     Qentinel
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

import xml.etree.ElementTree as ET

import click


@click.command()
@click.option('--verbose', '-v', is_flag=True)
@click.argument('filename')
def list_graph(verbose, filename):
    """List items from GRAPHML file."""
    tree = ET.parse(filename)
    root = tree.getroot()

    # pro tip: iterate over the tree with root.iter() to get right
    # name spaces for elements.

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

    sources = []
    for e in root.iter('{http://graphml.graphdrawing.org/xmlns}edge'):
        source = id2node[e.attrib["source"]]
        target = id2node[e.attrib["target"]]
        if verbose:
            print(source + ":" + target)
        sources.append(source)

        target_label = None
        for label in e.iter('{http://www.yworks.com/xml/graphml}EdgeLabel'):
            target_label = label.text
        if not nodes[source]["target"]:
            nodes[source]["target"] = [(target, target_label)]
        else:
            # multiple targets
            nodes[source]["target"].append((target, target_label))
    if verbose:
        print()
    for s in sources:
        print(s)
