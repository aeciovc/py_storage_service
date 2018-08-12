from nameko.rpc import rpc
from decouple import config
from logger import logger
from logging import error

from models import File
from storage_file_system import FileSystemStorage
from errors import InvalidConfigError
from storage import default_storage, config

import json

class StorageService:

    #Nameko Service
    name = config.NAME_SERVICE

    #RPC methods
    @rpc
    def ping(self):
        return "pong!"

    @rpc
    def get(self, uuid):

        #Reading file
        file_bytes = default_storage.get(uuid)
        
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
        uuid_name = default_storage.save(f.decode())
        return uuid_name

    @rpc
    def remove(self, uuid_name):

        try:
            default_storage.remove(uuid_name)
        except Exception as e:
            error("[StorageService] Error: {0}".format(e))
            return False

        return True