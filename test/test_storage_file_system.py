import unittest
import unittest.mock
import uuid
import os

from os import path
from unittest.mock import patch

from config import TestConfig
from storage_file_system import FileSystemStorage
from errors import InvalidConfigError, InvalidParamError
from logger import default

class CreateFileSystemStorageInstanceTestCase(unittest.TestCase):

    def test_create_instance_with_invalid_configs(self):

        with self.subTest("with no local storage"):
            with self.assertRaises(InvalidConfigError):
                config = TestConfig()
                config.LOCAL_STORAGE_LOCATION = ''

                FileSystemStorage(config)

        with self.subTest("with a relative path"):
            with self.assertRaises(InvalidConfigError):
                config = TestConfig()
                config.LOCAL_STORAGE_LOCATION = '../../etc'

                FileSystemStorage(config)

        with self.subTest("with None config"):
            with self.assertRaises(InvalidConfigError):
                FileSystemStorage(None)

        with self.subTest("with valid config"):

            config = TestConfig()

            storage = FileSystemStorage(config)

            from decouple import config
            BASE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '/test')

            self.assertEqual(storage.config.LOCAL_STORAGE_LOCATION, config('LOCAL_STORAGE_LOCATION'))

class TestRemove(unittest.TestCase):
    """
    Test remove function from the storage_file_system
    """

    def setUp(self):
        #Config
        self.config = TestConfig()

        #Storage
        self.storage = FileSystemStorage(self.config)

    def tearDown(self):
        self.config = None

    @patch("os.remove")
    def test_remove_success(self, remove):

        uuid_name = uuid.uuid4()

        #Assert return
        self.assertEqual(self.storage.remove(uuid_name), True)

        #Assert remove called
        param_called = path.join(self.config.LOCAL_STORAGE_LOCATION, str(uuid_name))
        remove.assert_called_with(param_called)

        
    @patch("os.remove")
    def test_remove_with_invalid_inputs(self, remove):
        
        with self.subTest("with integer"):
            with self.assertRaises(InvalidParamError):
                self.storage.remove(1)
                
                #Assert remove not called
                remove.assert_not_called()

        with self.subTest("with string not UUID"):
            with self.assertRaises(InvalidParamError):
                self.storage.remove("fegwegweg")

                #Assert remove not called
                remove.assert_not_called()
        
        with self.subTest("with None"):
            with self.assertRaises(InvalidParamError):
                self.storage.remove(None)

                #Assert remove not called
                remove.assert_not_called()

    def test_remove_no_file_found(self):

        with self.assertRaises(FileNotFoundError):
            self.storage.remove(uuid.uuid4())
        
if __name__ == '__main__':
    unittest.main()