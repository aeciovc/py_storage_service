
from logging import info, error
from os import path

import uuid
import io
import os

class StorageController(object):
    
    def __init__(self, config):
        self.config = config

    def get(self, uuid):
        
        if uuid:
            obj = self.read(uuid)
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

    def read(self, uuid_name):

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