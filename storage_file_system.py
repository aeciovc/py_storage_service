from logging import info, error
from os import path
from uuid import UUID

import uuid
import io
import os

from errors import InvalidConfigError, InvalidParamError

class FileSystemStorage(object):
    """
    Standard filesystem storage
    """

    def __init__(self, config):
        self.config = config

        if not self._is_valid_config():
            raise InvalidConfigError()

    def get(self, uuid):
        
        if uuid:
            obj = self._read(uuid)
            return obj
        else:
            return {}

    def save(self, uuid_name, raw_file):

        if not self._is_valid_uuid(uuid_name):
            raise InvalidParamError("This is not a uuid valid")

        if raw_file is None:
            raise InvalidParamError("Invalid file")

        #Path
        file_path = path.join(self.config.LOCAL_STORAGE_LOCATION, str(uuid_name))
        info("[Storage] Saving file: "+file_path)

        #Saving File
        try:
            f = io.open(file_path, 'wb')
            f.write(raw_file)
            f.close()
        except Exception as e:
            error("[Storage] Error trying read file"+ e.msg)
            return False

        info("[Storage] Saved")

        return True

    def remove(self, uuid_name):

        if not self._is_valid_uuid(uuid_name):
            raise InvalidParamError("This is not a UUID value")

        #Path
        file_path = path.join(self.config.LOCAL_STORAGE_LOCATION, str(uuid_name))
        info("[Storage] Removing file: "+file_path)

        #Removing File
        try:
            os.remove(file_path)
        except Exception as e:
            error("[Storage] Error trying remove file {0}".format(e))
            raise FileNotFoundError("File not found {0}".format(file_path))

        info("[Storage] Removed")

        return True

    #Private Functions
    def _read(self, uuid_name):

        if not uuid_name:
            return None
            
        file_path = path.join(self.config.LOCAL_STORAGE_LOCATION, uuid_name)

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
        if self.config is None or not hasattr(self.config, 'LOCAL_STORAGE_LOCATION') or self.config.LOCAL_STORAGE_LOCATION == '' or self._is_relative_path():
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
        if os.path.isdir(self.config.LOCAL_STORAGE_LOCATION):
            return True
        else:
            return False

    def _is_safe_path(self, path, follow_symlinks=True):
        if follow_symlinks:
            return os.path.realpath(path).startswith(self.config.LOCAL_STORAGE_LOCATION)

        return os.path.abspath(path).startswith(self.config.LOCAL_STORAGE_LOCATION)

    def _is_relative_path(self):
        return not os.path.isabs(self.config.LOCAL_STORAGE_LOCATION)
