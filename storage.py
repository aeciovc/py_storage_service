from logging import info, error, debug
from uuid import UUID
from config import DevelopmentConfig
from storage_file_system import FileSystemStorage
from storage_aws import AWSStorage

def __get_impl_class(_CLASS, config):

    if _CLASS == 'FileSystemStorage':

        return FileSystemStorage(config)

    elif _CLASS == 'AWSStorage':
        import boto3
        config.S3 = boto3.client(
            's3',
            aws_access_key_id = config.KEY,
            aws_secret_access_key = config.SECRET_KEY)

        return AWSStorage(config)

#Load Config
config = DevelopmentConfig()

#Load Type of Storage
default_storage = __get_impl_class(config.STORAGE_CLASS, config)

info("Initiliazing storage on "+ type(default_storage).__name__)
        