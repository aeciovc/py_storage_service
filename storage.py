from logging import info, error, debug

from uuid import UUID

from config import Config

from storage_aws import AWSStorage
from storage_file_system import FileSystemStorage

#Load Config
config = Config()
config.BUCKET_NAME = 'py-storage'

#Load Type of Storage
default_storage = AWSStorage(config)