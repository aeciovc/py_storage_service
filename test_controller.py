import unittest

from controller import StorageController
from models import StorageConfig
from errors import InvalidConfigError, InvalidParamError

import uuid

class TestGet(unittest.TestCase):
    """
    Test functions from the controller
    """

    #Config Search
    storage_config = StorageConfig("/home/user")
    storage_config_invalid = None

    def test_remove_with_invalid_config(self):

        storage = StorageController(self.storage_config_invalid)

        with self.assertRaises(InvalidConfigError):
            storage.remove(uuid.uuid4())
        
    def test_remove_with_invalid_inputs(self):
        
        storage = StorageController(self.storage_config)

        with self.subTest("with integer"):
            with self.assertRaises(InvalidParamError):
                storage.remove(1)

        with self.subTest("with string"):
            with self.assertRaises(InvalidParamError):
                storage.remove("fegwegweg")
        
        with self.subTest("with None"):
            with self.assertRaises(InvalidParamError):
                storage.remove(None)
        
if __name__ == '__main__':
    unittest.main()