import time

class Pauser(object):
    """ This is simple listener for Robot Framework,
        adding given delay in seconds (default 3 seconds)
        to each test step.

        Usage:
        robot --listener Pauser:5 test/
    """
    ROBOT_LISTENER_API_VERSION = 2

    def __init__(self, delay=3):
        self.delay = int(delay)

    def start_keyword(self, data, result):
        time.sleep(self.delay)
