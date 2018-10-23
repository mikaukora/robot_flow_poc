class Modifier(object):
    """ Usage:
        robot_flow get_tests.py test/test.robot > tests.txt
        (modify test list file)
        robot --listener Modifier:"tests.txt" test/
    """
    
    ROBOT_LISTENER_API_VERSION = 3

    def __init__(self, filename):
        print("Got filename: {}".format(filename))
        self.filename = filename
        self.tests = self.parse_tests(self.filename)
        
    def parse_tests(self, filename):
        with open(filename) as f:
            tests = f.readlines()
        print("Read {}".format(tests))
        return [t.strip() for t in tests]

    def start_suite(self, data, result):
        if data.tests:
            print("Original: {}".format(data.tests))
            print("Replacing with: {}".format(self.tests))

            modified = []
            # Find object from existing tests in a script and
            # move to a new list if still needed. It could be moved
            # to another location, removed or duplicated.
            for testname in self.tests:
                for old in data.tests:
                    if testname == old.name:
                        print("found")
                        modified.append(old)

            data.tests = modified
            print("Now using: {}".format(data.tests))

    def start_test(self, data, result):
        data.keywords.create(name='Log', args=['Keyword added by listener'])
        print("Keywords: {}".format(data.keywords))
            
    def end_test(self, data, result):
        print("Test ended")
