from logging import info, error
from os import path
from uuid import UUID

import uuid
import io
import os

from errors import InvalidConfigError, InvalidParamError

class StorageController(object):
    
    def __init__(self, config):
        self.config = config

    def get(self, uuid):
        
        if uuid:
            obj = self._read(uuid)
            return obj
        else:
            return {}

    def save(self, raw_file):

        #Generate id object
        uuid_name = str(uuid.uuid4())

        #Path
        file_path = path.join(self.config.location, uuid_name)
        info("[Storage] Saving file: "+file_path)

        #Saving File
        try:
            f = io.open(file_path, 'wb')
            f.write(raw_file)
            f.close()
        except Exception as e:
            error("[Storage] Error trying read file"+ e.msg)
            return None

        info("[Storage] Saved")

        return uuid_name

    def remove(self, uuid_name):

        if not self._is_valid_config():
            raise InvalidConfigError()

        if not self._is_valid_uuid(uuid_name):
            raise InvalidParamError("This is not a UUID value")

        #Path
        file_path = path.join(self.config.location, uuid_name)
        info("[Storage] Removing file: "+file_path)

        #Removing File
        try:
            os.remove(file_path)
        except Exception as e:
            error("[Storage] Error trying remove file"+ e.msg)
            return False

        info("[Storage] Removed")

        return True

    #Private Functions
    def _read(self, uuid_name):

        if not uuid_name:
            return None
            
        file_path = path.join(self.config.location, uuid_name)

        if path.isfile(file_path):
            info("[Storage] Reading from: "+ file_path)
            
            try:
                f = io.open(file_path, 'rb').read()
                return f
            except Exception as e:
                error("[Storage] Error trying read file"+ e.msg)
                return None
        else:
            error("[Storage] File not found: "+ file_path)
            return None

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
