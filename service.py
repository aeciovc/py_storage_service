from nameko.rpc import rpc
from decouple import config

from models import StorageConfig, File
from controller import StorageController

import json

#Intern Modules
from logger import default

class StorageService:
    name = config('SERVICE_NAME')

    #Configs
    LOCAL_STORAGE_LOCATION = config('LOCAL_STORAGE_LOCATION')

    #RPC methods
    @rpc
    def ping(self):
        return "pong!"

    @rpc
    def get(self, uuid):

        #Config Search
        storage_config = StorageConfig(self.LOCAL_STORAGE_LOCATION)

        #Reading file
        file_bytes = StorageController(storage_config).get(uuid)
        
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
        
        #Config Search
        storage_config = StorageConfig(self.LOCAL_STORAGE_LOCATION)

        #Save File
        uuid_name = StorageController(storage_config).save(f.decode())
        return uuid_name