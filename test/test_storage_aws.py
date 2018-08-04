import unittest
import tempfile

from mock.mock import MagicMock
from unittest.mock import patch
from decouple import config as confdecouple
from logger import default

from storage_aws import AWSStorage
from config import Config
from errors import InvalidConfigError, InvalidParamError, AWSExceptionError
from config import Config, TestConfig

class CreateAWSStorageInstanceTestCase(unittest.TestCase):

    def test_create_instance_with_invalid_configs(self):

        with self.subTest("with no bucket name"):
            with self.assertRaises(InvalidConfigError):
                config = TestConfig()
                config.KEY = confdecouple('KEY')
                config.SECRET_KEY = confdecouple('SECRET_KEY')        

                AWSStorage(config)

        with self.subTest("with no key"):
            with self.assertRaises(InvalidConfigError):
                config = TestConfig()
                config.BUCKET_NAME = confdecouple('BUCKET_NAME')
                config.SECRET_KEY = confdecouple('SECRET_KEY')

                AWSStorage(config)

        with self.subTest("with no secret key"):
            with self.assertRaises(InvalidConfigError):
                config = TestConfig()
                config.BUCKET_NAME = confdecouple('BUCKET_NAME')
                config.KEY = confdecouple('KEY')

                AWSStorage(config)

        with self.subTest("with None config"):
            with self.assertRaises(InvalidConfigError):
                AWSStorage(None)

        with self.subTest("with valid config"):

            config = TestConfig()
            config.BUCKET_NAME = confdecouple('BUCKET_NAME')
            config.KEY = confdecouple('KEY')
            config.SECRET_KEY = confdecouple('SECRET_KEY')

            storage = AWSStorage(config)

            self.assertEqual(storage.config.BUCKET_NAME, confdecouple('BUCKET_NAME'))
            self.assertEqual(storage.config.KEY, confdecouple('KEY'))
            self.assertEqual(storage.config.SECRET_KEY, confdecouple('SECRET_KEY'))

class SaveWithInvalidParamsTestCase(unittest.TestCase):

    def setUp(self):

        #Config
        config = TestConfig()
        config.BUCKET_NAME = confdecouple('BUCKET_NAME')
        config.KEY = confdecouple('KEY')
        config.SECRET_KEY = confdecouple('SECRET_KEY')

        #Mock
        mock = MagicMock()
        mock.put_object(Bucket=config.BUCKET_NAME, Key='d20b1c38-2f5f-4b48-b604-eb90f82ff800', Body=b'It is a file!')
        mock.put_object.side_effect = Exception()

        #Temp File
        self.file = tempfile.TemporaryFile(mode='w+b')
        self.file.write(b'It is a file!')
        self.file.seek(0)
        self.raw_file = self.file.read()

        config.S3 = mock

        #Storage
        self.storage = AWSStorage(config)
        self.config = config

    def tearDown(self):
        self.storage = None
        self.file.close()

    def test_with_invalid_file(self):

        #Input
        uuid_name = 'd20b1c38-2f5f-4b48-b604-eb90f82ff800'

        with self.assertRaises(InvalidParamError):
            self.storage.save(uuid_name, None)

    def test_with_invalid_uuid(self):
        
        #Input
        body = self.raw_file

        with self.assertRaises(InvalidParamError):
            self.storage.save(None, body)

    def test_with_aws_error(self):

        #Input
        uuid_name = 'd20b1c38-2f5f-4b48-b604-eb90f82ff800'
        body = self.raw_file

        #Validate AWS call
        self.storage.config.S3.put_object.assert_called_with(Body=body, Bucket=self.config.BUCKET_NAME, Key=uuid_name)
       
        with self.assertRaises(AWSExceptionError):
            self.storage.save(uuid_name, self.raw_file)

class SaveSuccessTestCase(unittest.TestCase):
    def setUp(self):
        
        #Temp File
        self.file = tempfile.TemporaryFile(mode='w+b')
        self.file.write(b'It is a file!')
        self.file.seek(0)
        self.raw_file = self.file.read()

        #Config
        config = TestConfig()
        config.BUCKET_NAME = confdecouple('BUCKET_NAME')
        config.KEY = confdecouple('KEY')
        config.SECRET_KEY = confdecouple('SECRET_KEY')

        #Mock
        mock = MagicMock()
        mock.put_object(Bucket=config.BUCKET_NAME, Key='d20b1c38-2f5f-4b48-b604-eb90f82ff800', Body=b'It is a file!')

        config.S3 = mock

        #Storage
        self.storage = AWSStorage(config)
        self.config = config
    
    def tearDown(self):
        self.storage = None
        self.file.close()

    def test_save_success(self):

        uuid_name = 'd20b1c38-2f5f-4b48-b604-eb90f82ff800'
        body = self.raw_file

        #Save
        result = self.storage.save(uuid_name, self.raw_file)

        #Validate aws call and result
        self.storage.config.S3.put_object.assert_called_with(Body=body, Bucket=self.config.BUCKET_NAME, Key=uuid_name)
        self.assertTrue(result)

    """
class SaveTestCase(ConfigTest):
    
    Test save function to the storage_aws
    
    @patch('botocore.client', return_value=True)
    def test_save_success(self, mock_put_object):

        #Temp File
        f = tempfile.TemporaryFile(mode='w+b')
        f.write(b'It is a file!')
        f.seek(0)
        raw_file = f.read()

        id = self.storage.save(raw_file)
        print("ID generated: ", id)

        # verify
        mock_put_object.assert_called_with(message="Hello World!")
    """

class RemoveWithInvalidParamsTestCase(unittest.TestCase):

    def setUp(self):

        #Config
        config = TestConfig()
        config.BUCKET_NAME = confdecouple('BUCKET_NAME')
        config.KEY = confdecouple('KEY')
        config.SECRET_KEY = confdecouple('SECRET_KEY')

        #Mock
        mock = MagicMock()
        mock.delete_object(Bucket=config.BUCKET_NAME, Key='d20b1c38-2f5f-4b48-b604-eb90f82ff800')
        mock.delete_object.side_effect = Exception()

        config.S3 = mock

        #Storage
        self.storage = AWSStorage(config)
        self.config = config

    def tearDown(self):
        self.storage = None

    def test_with_invalid_uuid(self):
        
        with self.subTest("with none"):
            with self.assertRaises(InvalidParamError):
                self.storage.remove(None)

        with self.subTest("with integer"):
            with self.assertRaises(InvalidParamError):
                self.storage.remove(1)

        with self.subTest("with string not UUID"):
            with self.assertRaises(InvalidParamError):
                self.storage.remove("fegwegweg")

    def test_with_aws_error(self):

        #Input
        uuid_name = 'd20b1c38-2f5f-4b48-b604-eb90f82ff800'

        #Validate AWS call
        self.storage.config.S3.delete_object.assert_called_with(Bucket=self.config.BUCKET_NAME, Key=uuid_name)
       
        with self.assertRaises(AWSExceptionError):
            self.storage.remove(uuid_name)

class RemoveSuccessTestCase(unittest.TestCase):
    def setUp(self):
        
        #Config
        config = TestConfig()
        config.BUCKET_NAME = confdecouple('BUCKET_NAME')
        config.KEY = confdecouple('KEY')
        config.SECRET_KEY = confdecouple('SECRET_KEY')

        #Mock
        mock = MagicMock()
        mock.delete_object(Bucket=config.BUCKET_NAME, Key='d20b1c38-2f5f-4b48-b604-eb90f82ff800')

        config.S3 = mock

        #Storage
        self.storage = AWSStorage(config)
        self.config = config
    
    def tearDown(self):
        self.storage = None

    def test_save_success(self):

        uuid_name = 'd20b1c38-2f5f-4b48-b604-eb90f82ff800'

        #Remove
        result = self.storage.remove(uuid_name)

        #Validate aws call and result
        self.storage.config.S3.delete_object.assert_called_with(Bucket=self.config.BUCKET_NAME, Key=uuid_name)
        self.assertTrue(result)
    
if __name__ == '__main__':
    unittest.main()