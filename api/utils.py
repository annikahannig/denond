

"""
Helper functions
"""

import re
import time
import threading

from Queue import Queue

def round_halfstep(value):
    """Round value to 0.5 for half steps"""
    return round(value * 2.0) / 2.0


def pack_float(value):
    """Pack float value into 3 byte ascii"""
    result = "%02d" % value + str(value%1)[1:3]
    sval = re.sub(r'\D', '', result)
    return sval


def limit_range(minval, maxval, value):
    """Limit the value to a fixed range"""
    if value > maxval:
        value = maxval
    if value < minval:
        value = minval
    return value


def numeric_value(value):
    """Get numeric value from response"""
    sval = re.sub(r'\D', '', value)
    val = float(sval)
    if val > 100:
        val = val / 10.0
    return val


def boolean_value(value):
    """Get boolean value from response"""
    return "ON" in value


def string_value(value):
    return value[2:].strip()


class Service(object):
    """Minimal GenServer like actor for handling uploads"""

    def __init__(self, parent=None):
        """Initialize service"""
        self.mailbox = Queue()
        self.runner = None
        self.parent = parent


    def spawn(self, *args, **kwargs):
        """Start thread"""
        if self.runner:
            return

        self.runner = threading.Thread(target=self.main)
        self.runner.start()

        # Invoke setup callback
        self.init(*args, **kwargs)

        return self



    def terminate(self):
        """Shutdown"""
        self.send('end')
        self.runner.join()
        return self


    def main(self):
        """Gen server like default behaviour"""
        for message in self.receive():
            if type(message) is not tuple:
                raise Exception("Unexpected input")
            if message[0] == 'cast':
                self.handle_cast(message[1])
            elif message[0] == 'call':
                replies = message[1]
                result = self.handle_call(message[2])
                replies.put(result)


    def send(self, message):
        """Add a message to the queue"""
        self.mailbox.put(message)
        return self


    def receive(self):
        """Read from queue"""
        while True:
            message = self.mailbox.get()
            if message == 'end':
                return
            yield message


    def call(self, action):
        """Sync interaction"""
        replies = Queue()
        self.send(('call', replies, action))

        # Get response
        return replies.get()


    def cast(self, action):
        """Async interaction"""
        return self.send(('cast', action))


    def init(self):
        """Initialize callback"""
        pass


    def handle_call(self, action):
        """Handle sync action"""
        return False


    def hadle_cast(self, action):
        """Handle async action"""
        pass


