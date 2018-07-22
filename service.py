from nameko.rpc import rpc
from decouple import config

from models import StorageConfig, File
from controller import StorageController
from errors import InvalidConfigError

import json

#Intern Modules
from logger import default

from logging import error

class StorageService:
    name = config('SERVICE_NAME')

    #Configs
    LOCAL_STORAGE_LOCATION = config('LOCAL_STORAGE_LOCATION')

    #Config Storage
    storage_config = StorageConfig(LOCAL_STORAGE_LOCATION)

    #RPC methods
    @rpc
    def ping(self):
        return "pong!"

    @rpc
    def get(self, uuid):

        #Reading file
        file_bytes = StorageController(self.storage_config).get(uuid)
        
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
        uuid_name = StorageController(self.storage_config).save(f.decode())
        return uuid_name

    @rpc
    def remove(self, uuid_name):

        try:
            StorageController(self.storage_config).remove(uuid_name)
        except InvalidConfigError as e:
            error("[StorageService] Error: "+ e.msg)
            return False

        return True