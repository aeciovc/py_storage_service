from nameko.rpc import rpc
from decouple import config

from models import File
from storage_file_system import FileSystemStorage
from errors import InvalidConfigError
from config import DevelopmentConfig
from logger import default
from logging import error

import json

class StorageService:

    #Config Storage
    storage_config = DevelopmentConfig()

    #Nameko Service
    name = storage_config.NAME_SERVICE

    #RPC methods
    @rpc
    def ping(self):
        return "pong!"

    @rpc
    def get(self, uuid):

        #Reading file
        file_bytes = FileSystemStorage(self.storage_config).get(uuid)
        
        if file_bytes is not None:
            #Build object
            f = File(file_bytes)
            return f.encode().as_json()
        else:
            return None

    @rpc
    def save(self, file):

        json_file = json.loads(file)

        f = File(json_file["content"])
        
        #Save File
        uuid_name = FileSystemStorage(self.storage_config).save(f.decode())
        return uuid_name

    @rpc
    def remove(self, uuid_name):

        try:
            FileSystemStorage(self.storage_config).remove(uuid_name)
        except Exception as e:
            error("[StorageService] Error: {0}".format(e))
            return False

        return True