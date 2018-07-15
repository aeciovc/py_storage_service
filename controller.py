
import uuid
import io

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

        print ("[Storage] Saving file: "+uuid_name)

        #Saving File
        f = io.open(self.config.location+"/"+uuid_name,'wb')
        f.write(raw_file)
        f.close()

        print ("[Storage] Saved")

        return uuid_name

    def read(self, uuid_name):

        if uuid_name:
            path = self.config.location+"/"+uuid_name

            print("[Storage] Reading from: ", self.config.location+"/"+uuid_name)
            f = io.open(path, 'rb').read()
            return f
        else:
            return None