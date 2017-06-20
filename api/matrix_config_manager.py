
"""
Audiomatrix configuration manager
"""
import time
import os

from glob import glob

import denon

from utils import Service



class ConfigUploader(Service):
    """Handle Uploads"""
    def start(self, host):
        """Initialize service"""
        self.client = denon.Client(host)
        print("[i] Config uploader initialized")


    def handle_cast(self, action):
        """Just start the upload"""
        self.parent.cast(('UPLOAD_START', None))
        print("Uploading " + action)
        time.sleep(5)
        self.parent.cast(('UPLOAD_DONE', None))


    #
    # API
    #
    def upload(self, filename):
        self.cast(filename)


class ConfigManager(Service):
    """Manage audio matrix configurations"""

    def start(self, host, configs_path=None):
        """Initialize service"""
        if not configs_path:
            configs_path = os.path.join(os.path.dirname(__file__),
                                       '../mappings')

        self.configs_path = configs_path

        # Uploader
        self.uploader = ConfigUploader(self).spawn(host)

        # State
        self.is_uploading = False


    def terminate(self):
        """Override default terminate to include child"""
        self.uploader.terminate()
        super(ConfigManager, self).terminate()


    def handle_call(self, action):
        """React to sync calls"""
        (request, payload) = action
        if request == 'LIST_CONFIGURATIONS':
            return self._fetch_configurations()
        elif request == 'GET_UPLOAD_STATE':
            return self._get_upload_state()


    def handle_cast(self, action):
        """Async requests"""
        (request, payload) = action
        if request == 'UPLOAD_REQUEST':
            self.is_uploading = True
            self.uploader.upload(payload)
        elif request == 'UPLOAD_DONE':
            self.is_uploading = False
        elif request == 'UPLOAD_ERROR':
            self.is_uploading = False
            self.upload_error = payload


    def _get_upload_state(self):
        """Get current upload state"""
        return {
            'is_uploading': self.is_uploading,
        }


    def _fetch_configurations(self):
        """Get list of configs"""
        return glob(self.configs_path + '/*.yml')


    #
    # API
    #
    def list_configurations(self):
        """Return list of available configurations"""
        return self.call(('LIST_CONFIGURATIONS', None))


    def upload(self, filename):
        if self.is_uploading:
            return 'is_uploading'
        self.cast(('UPLOAD_REQUEST', filename))
        return 'upload_requested'


    def get_upload_state(self):
        return self.call(('GET_UPLOAD_STATE', None))
