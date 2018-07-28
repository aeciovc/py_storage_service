from logging import info, error
from os import path
from uuid import UUID

import uuid
import io
import os

from errors import InvalidConfigError, InvalidParamError

class StorageControllerAWS(object):
    
    def __init__(self, config):
        self.config = config

    def get(self, uuid):
        
        if uuid:
            obj = self._read(uuid)
            return obj
        else:
            return {}

    def save(self, raw_file):
        pass
        

    def remove(self, uuid_name):
        pass

        
    def _is_valid_config(self):
        if not hasattr(self.config, 'location'):
            return False
        else:
            return True
        
    def _is_valid_uuid(self, uuid_name):
        try:
            if UUID(str(uuid_name)).version:
                return True
        except ValueError:
            return False

    def _is_path_exists(self):
        if os.path.isdir(self.config.location):
            return True
        else:
            return False
