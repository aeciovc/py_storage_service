import unittest
import unittest.mock
import uuid
import os
import tempfile

from os import path
from unittest.mock import patch, Mock

from config import TestConfig
from storage_file_system import FileSystemStorage
from errors import InvalidConfigError, InvalidParamError, FileNotFoundError
from logger import logger

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

class RemoveTestCase(unittest.TestCase):
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

    @patch("os.remove")
    def test_remove_no_file_found(self, remove):

        uuid_name = uuid.uuid4()

        remove.side_effect = OSError()

        with self.assertRaises(FileNotFoundError):
            self.storage.remove(uuid_name)

        #Assert remove called
        param_called = path.join(self.config.LOCAL_STORAGE_LOCATION, str(uuid_name))
        remove.assert_called_with(param_called)

class SaveTestCase(unittest.TestCase):
    """
    Test save function from the storage_file_system
    """

    def setUp(self):
        #Config
        self.config = TestConfig()

        #Storage
        self.storage = FileSystemStorage(self.config)

        #Temp File
        self.file = tempfile.TemporaryFile(mode='w+b')
        self.file.write(b'It is a file!')
        self.file.seek(0)
        self.raw_file = self.file.read()

    def tearDown(self):
        self.config = None

    @patch("io.open")
    def test_save_success(self, open):

        uuid_name = uuid.uuid4()

        #Assert return
        self.assertEqual(self.storage.save(uuid_name, self.file), True)

        #Assert save called
        param_called = path.join(self.config.LOCAL_STORAGE_LOCATION, str(uuid_name))
        open.assert_called_with(param_called, 'wb')

        
    @patch("io.open")
    def test_save_with_invalid_inputs(self, open):
        
        with self.subTest("with integer"):
            with self.assertRaises(InvalidParamError):
                self.storage.save(1, self.file)
                
                #Assert open not called
                open.assert_not_called()

        with self.subTest("with string not UUID"):
            with self.assertRaises(InvalidParamError):
                self.storage.save("fegwegweg", self.file)

                #Assert open not called
                open.assert_not_called()
        
        with self.subTest("with None"):
            with self.assertRaises(InvalidParamError):
                self.storage.save(None, self.file)

                #Assert open not called
                open.assert_not_called()

        with self.subTest("with invalid file"):
            with self.assertRaises(InvalidParamError):
                self.storage.save(uuid.uuid4(), None)

                #Assert open not called
                open.assert_not_called()

class GetTestCase(unittest.TestCase):
    """
    Test get function from the storage_file_system
    """

    def setUp(self):
        #Config
        self.config = TestConfig()

        #Storage
        self.storage = FileSystemStorage(self.config)

        #Temp File
        self.file = tempfile.TemporaryFile(mode='w+b')
        self.file.write(b'It is a file!')
        self.file.seek(0)
        self.raw_file = self.file.read()

    def tearDown(self):
        self.config = None

    @patch.object(FileSystemStorage, '_read', autospec=True)
    def test_get_success(self, read):
        
        uuid_name = uuid.uuid4()

        #Mock result
        read.return_value=self.raw_file

        #Assert return
        self.assertEqual(self.storage.get(uuid_name), self.raw_file)

        #Assert read called
        read.assert_called_with(self.storage, uuid_name)
        
    @patch.object(FileSystemStorage, '_read', autospec=True)
    def test_get_with_invalid_inputs(self, read):
        
        with self.subTest("with integer"):
            with self.assertRaises(InvalidParamError):
                self.storage.get(1)
                
                #Assert open not called
                read.assert_not_called()

        with self.subTest("with string not UUID"):
            with self.assertRaises(InvalidParamError):
                self.storage.get("sdgsdg")

                #Assert open not called
                read.assert_not_called()
        
        with self.subTest("with None"):
            with self.assertRaises(InvalidParamError):
                self.storage.get(None)

                #Assert open not called
                read.assert_not_called()

    @patch.object(FileSystemStorage, '_read', autospec=True)
    def test_get_no_file_found(self, read):

        uuid_name = uuid.uuid4()

        #Mock result
        read.return_value = None

        with self.assertRaises(FileNotFoundError):
            self.storage.get(uuid_name)

        #Assert read called
        read.assert_called_with(self.storage, uuid_name)

if __name__ == '__main__':
    unittest.main()