import unittest
import unittest.mock

from unittest.mock import patch

import uuid

from controller import StorageController
from models import StorageConfig
from errors import InvalidConfigError, InvalidParamError

#Intern Modules
from logger import default
#from logging import debug

class TestRemove(unittest.TestCase):
    """
    Test remove function from the controller
    """

    #Config
    storage_config = StorageConfig("/home/user")
    storage_config_invalid = None

    @patch('controller.StorageController.remove', return_value=True)
    def test_remove_success(self, remove):

        storage = StorageController(self.storage_config)

        self.assertEqual(storage.remove(uuid.uuid4()), True)

    def test_remove_with_invalid_config(self):

        storage = StorageController(self.storage_config_invalid)

        with self.assertRaises(InvalidConfigError):
            storage.remove(uuid.uuid4())
        
    def test_remove_with_invalid_inputs(self):
        
        storage = StorageController(self.storage_config)

        with self.subTest("with integer"):
            with self.assertRaises(InvalidParamError):
                storage.remove(1)

        with self.subTest("with string not UUID"):
            with self.assertRaises(InvalidParamError):
                storage.remove("fegwegweg")
        
        with self.subTest("with None"):
            with self.assertRaises(InvalidParamError):
                storage.remove(None)

    def test_remove_no_file_found(self):

        storage = StorageController(self.storage_config)

        with self.assertRaises(FileNotFoundError):
            storage.remove(uuid.uuid4())
        
if __name__ == '__main__':
    unittest.main()