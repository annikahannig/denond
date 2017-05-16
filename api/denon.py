
"""
Denon telnet api client
"""

import socket

class Client(object):
    def __init__(self, host, port):
        """Create new client"""
        self.host = host
        self.port = port

    def call(self, command, params=""):
        """Connect to denon and send command, receive response"""
        conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        conn.connect((self.host, self.port))

        # Send command
        tx = conn.send("{}{}\r".format(command, params))
        if tx == 0:
            raise RuntimeError("connection lost")

        # Receive response
        res = conn.recv(256)
        if res == b'':
            raise RuntimeError("connection lost")

        conn.close()

        return res

