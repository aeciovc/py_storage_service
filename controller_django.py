from .models import StorageConfig
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

class StorageController(object):

    def __init__(self, config):
        self.config = config

    def save(self, raw_file, file_name):
        print ("[Storage] Saving file: "+file_name)
        path = default_storage.save(self.config.location+"/"+file_name, ContentFile(raw_file))
        print ("[Storage] Saved: "+path)

        return True

    def read(self, uuid_name):

        if uuid_name:
            #Get image from hash
            path = self.config.location+"/"+uuid_name
            print("[Storage] Reading from: ",default_storage)
            image_data = default_storage.open(path).read()
            return image_data
        else:
            return self.get_default_image()
            

    def get_default_image(self):
        #Get image default
        path = self.config.location+"/"+self.config.default_product_image_name
        print("[Storage] Reading from: ", default_storage)
        image_data = default_storage.open(path).read()
        return image_data