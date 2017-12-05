
"""
Denon telnet api and web "api" client
"""

import socket
import time
import requests

from denond import matrix_config
from denond import utils
from denond.webinterface import scraper
from denond.matrix_config import MatrixConfig

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


    def write_matrix_config(self, matrix):
        """Write an audio matrix configuration"""
        base_path = 'SETUP/INPUTS/INPUTASSIGN'
        endpoints = ['s_InputAssignHDMI.asp',
                     's_InputAssignDIGITAL.asp',
                     's_InputAssignCOMP.asp',
                     's_InputAssignANALOG.asp',
                     's_InputAssignVIDEO.asp']

        inputs = [matrix_config.INPUT_HDMI,
                  matrix_config.INPUT_DIGITAL,
                  matrix_config.INPUT_COMP,
                  matrix_config.INPUT_ANALOG,
                  matrix_config.INPUT_VIDEO]

        base_url = 'http://{}/{}'.format(self.host, base_path)


        for inp, endpoint in zip(inputs, endpoints):
            url = "{}/{}".format(base_url, endpoint)

            params = matrix.get_input_mapping(inp)

            if not params:
                continue

            params['setPureDirectOn'] = 'OFF'
            params['setSetupLock'] = 'OFF'

            for _, _ in params.items():
                res = requests.post(url, data=params)


    def read_matrix_config(self):
        """Read an audio matrix configuration"""
        endpoint = 'http://{}/{}'.format(
            self.host,
            'SETUP/INPUTS/INPUTASSIGN/d_InputAssign.asp')

        html = requests.get(endpoint).text
        matrix = scraper.parse_assigned_inputs(html)

        config = MatrixConfig(matrix)
        return config


    def update_matrix_config(self, matrix):
        """Write diff of matrix config"""
        current = self.read_matrix_config()
        diff = matrix.diff(current)
        self.write_matrix_config(diff)


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
