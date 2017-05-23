
"""
Denon telnet api client
"""

import socket
import utils
import time


COMMAND_TIMEOUT = 0.135

MAIN_ZONE_ON  = "ON"
MAIN_ZONE_OFF = "OFF"


class AmpOfflineException(Exception):
    pass


class Client(object):
    def __init__(self, host, port=23):
        """Create new client"""
        self.host = host
        self.port = port

        self.cache = dict() # Cache responses


    def call(self, command, result_count=1):
        """Connect to denon and send command, receive response"""
        # Connect to amp with short timeout:
        # "The RESPONSE should be sent within 200ms of
        # receiving the COMMAND."
        try:
            conn = socket.create_connection((self.host, self.port),
                                            timeout=0.20)
        except:
            raise AmpOfflineException()

        # Send command
        tx = conn.send("{}\r".format(command))
        if tx == 0:
            return self.get_cached(command)

        result = []

        # Receive response
        try:
            for _ in range(result_count):
                res = conn.recv(256)
                if not res:
                    break
                result.append(res)
        except socket.timeout as e:
            return self.get_cached(command)

        conn.close()

        # cache response
        self.cache[command] = result

        return result


    def cast(self, command):
        """Send a command without awaiting any response"""
        try:
            conn = socket.create_connection((self.host, self.port),
                                            timeout=0.20)
        except:
            return False

        # Send command
        tx = conn.send("{}\r".format(command))
        if tx == 0:
            return False

        conn.close()
        return True # We are done


    def get_cached(self, command):
        """Get cached response"""
        return self.cache.get(command)


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
        time.sleep(COMMAND_TIMEOUT)

        # Set volume
        self.cast("MV" + utils.pack_float(value))
        return value


    def get_main_zone_on(self):
        """Query main zone status"""
        try:
            res = self.call("ZM?")
            is_on = utils.boolean_value(res[0])
        except AmpOfflineException:
            is_on = False

        return is_on


    def set_main_zone_state(self, state):
        """Set main zone ON or OFF"""
        self.cast("ZM" + state)


    def get_main_zone_source(self):
        """Get selected input source"""
        res = self.call("SI?")
        return utils.string_value(res[0])


    def get_main_zone_state(self):
        """Get main zone state: on/off, volume and source"""
        on = self.get_main_zone_on()
        time.sleep(COMMAND_TIMEOUT)
        volume = self.get_master_volume()
        time.sleep(COMMAND_TIMEOUT)
        source = self.get_main_zone_source()

        state = {
            "on": on,
            "volume": volume,
            "source": source
        }

        return state
