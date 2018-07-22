import unittest

from controller import StorageController
import models
import errors

import uuid

class TestGet(unittest.TestCase):
    """
    Test functions from the controller
    """

    #Config Search
    storage_config = None
    invalid_storage_config = None

    def test_remove_with_invalid_config(self):

        storage = StorageController(self.invalid_storage_config)

        with self.assertRaises(errors.InvalidConfigError):
            storage.remove(uuid.uuid4())

    '''
    def test_remove_with_integer(self):
        
        result = StorageController(self.storage_config).remove(1)
        self.assertEqual(result, 0)
    '''

if __name__ == '__main__':
    unittest.main()