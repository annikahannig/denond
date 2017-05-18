
"""
Denon telnet api client
"""

import socket
import utils
import time

class Client(object):
    def __init__(self, host, port=23):
        """Create new client"""
        self.host = host
        self.port = port

    def call(self, command, params="", result_count=1):
        """Connect to denon and send command, receive response"""
        # Connect to amp with short timeout:
        # "The RESPONSE should be sent within 200ms of
        # receiving the COMMAND."
        conn = socket.create_connection((self.host, self.port),
                                        timeout=0.25)

        # Send command
        tx = conn.send("{}{}\r".format(command, params))
        if tx == 0:
            raise RuntimeError("connection lost")

        result = []

        # Receive response
        try:
            for _ in range(result_count):
                res = conn.recv(256)
                if not res:
                    break
                result.append(res)
        except socket.timeout as e:
            result = ["0"]

        conn.close()

        return result


    def get_master_volume(self):
        """Read the master volume"""
        res = self.call("MV?")
        return utils.numeric_value(res[0])


    def set_master_volume(self, value):
        """Sets the master volume"""
        # Limit value to allowed range
        value = utils.limit_range(0, 98, value)

        # The amp hangs if the value does not change.
        # So, check the value before sending the command.
        value = utils.round_halfstep(value)
        current_value = self.get_master_volume()
        if value == current_value:
            return value

        # Wait a bit
        time.sleep(0.1)

        # Set volume
        res = self.call("MV", utils.pack_float(value))
        return utils.numeric_value(res[0])


