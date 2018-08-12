from logging import info, error
from os import path
from uuid import UUID

import uuid
import io
import os

from errors import InvalidConfigError, InvalidParamError, FileNotFoundError, FileSystemExceptionError

class FileSystemStorage(object):
    """
    Standard filesystem storage
    """

    def __init__(self, config):
        self.config = config

        if not self._is_valid_config():
            raise InvalidConfigError()

    def get(self, uuid_name):
        
        if not self._is_valid_uuid(uuid_name):
            raise InvalidParamError("This is not a UUID value")

        obj = self._read(uuid_name)

        if obj is None:
            raise FileNotFoundError("{0}".format(uuid_name))
        
        return obj

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
            error("[Storage] Error trying read file {0}".format(e))
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
        except OSError as e:
            error("[Storage] Error trying remove file {0}".format(e))
            raise FileNotFoundError("{0}".format(file_path))
        except Exception as e:
            error("[Storage] Error trying remove file {0}".format(e))
            raise Exception("Unknown error {0}".format(file_path))

        info("[Storage] Removed")

        return True

    #Private Functions
    def _read(self, uuid_name):

        if not uuid_name:
            return None
            
        file_path = path.join(self.config.LOCAL_STORAGE_LOCATION, str(uuid_name))

        if path.isfile(file_path):
            info("[Storage] Reading from: "+ file_path)

            try:
                f = io.open(file_path, 'rb')
                return f.read()
            except Exception as e:
                error("[Storage] Error trying read file {0}".format(e))
                raise FileSystemExceptionError(" Error trying read file {0}".format(file_path))
        else:
            error("[Storage] File not found {0}".format(file_path))
            raise FileNotFoundError("{0}".format(file_path))

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
