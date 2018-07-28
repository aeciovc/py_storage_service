import unittest
import unittest.mock
import uuid
import io
import tempfile

from unittest.mock import patch
from decouple import config as confdecouple

#from storage import default_storage
from storage_aws import AWSStorage
from config import Config
from errors import InvalidConfigError, InvalidParamError

#Intern Modules
#from logger import default
#from logging import debug

class ConfigTest(unittest.TestCase):
    def setUp(self):
        
        #Config
        config = Config()
        config.BUCKET_NAME = confdecouple('BUCKET_NAME')
        config.KEY = confdecouple('KEY')
        config.SECRET_KEY = confdecouple('SECRET_KEY')

        #Storage
        self.storage = AWSStorage(config)
        self.storage_invalid_config = AWSStorage(None)

    def tearDown(self):
        self.storage = None
        self.storage_invalid_config = None

class SaveTestCase(ConfigTest):
    """
    Test save function to the storage_aws
    """

    def test_save_success(self):

        #Temp File
        f = tempfile.TemporaryFile(mode='w+b')
        f.write(b'It is a file!')
        f.seek(0)
        raw_file = f.read()

        id = self.storage.save(raw_file)
        print("ID generated: ", id)

class RemoveTestCase(ConfigTest):
    """
    Test remove function from the storage_aws
    """

    def test_remove_success(self):
        self.assertEqual(self.storage.remove('9135e7b9-a996-4c1d-9a3e-9ffb0277999d'), True)

    def test_remove_with_invalid_config(self):

        with self.assertRaises(InvalidConfigError):
            self.storage_invalid_config.remove(uuid.uuid4())
        
    def test_remove_with_invalid_inputs(self):
        
        with self.subTest("with integer"):
            with self.assertRaises(InvalidParamError):
                self.storage.remove(1)

        with self.subTest("with string not UUID"):
            with self.assertRaises(InvalidParamError):
                self.storage.remove("fegwegweg")
        
        with self.subTest("with None"):
            with self.assertRaises(InvalidParamError):
                self.storage.remove(None)

    def test_remove_no_file_found(self):
        self.assertEqual(self.storage.remove(uuid.uuid4()), True) #It's a default behavior on AWS
    
if __name__ == '__main__':
    unittest.main()