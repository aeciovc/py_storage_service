import unittest
import unittest.mock
import uuid

from unittest.mock import patch

from storage_file_system import FileSystemStorage
from models import StorageConfig
from errors import InvalidConfigError, InvalidParamError
from logger import default

class TestRemove(unittest.TestCase):
    """
    Test remove function from the storage_file_system
    """

    def setUp(self):
        self.storage_config = StorageConfig("/home/user")
        self.storage_config_invalid = None

    def tearDown(self):
        self.storage_config = None
        self.storage_config_invalid = None

    @patch('storage_file_system.FileSystemStorage.remove', return_value=True)
    #@patch("os.remove") fazer dessa forma e mocar apenas a chamada do SO
    def test_remove_success(self, remove):

        storage = FileSystemStorage(self.storage_config)

        self.assertEqual(storage.remove(uuid.uuid4()), True)

        #os_mock.write.assert_called_once_with("some debug message here") garanta que o SO foi chamada uma vez
        #exit_mock.assert_not_called() caso exista outra função que nesse teste não deveria ter sido chamada

    def test_remove_with_invalid_config(self):

        storage = FileSystemStorage(self.storage_config_invalid)

        with self.assertRaises(InvalidConfigError):
            storage.remove(uuid.uuid4())
        
    def test_remove_with_invalid_inputs(self):
        
        storage = FileSystemStorage(self.storage_config)

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

        storage = FileSystemStorage(self.storage_config)

        with self.assertRaises(FileNotFoundError):
            storage.remove(uuid.uuid4())
        
if __name__ == '__main__':
    unittest.main()