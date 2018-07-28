from logging import info, error
from os import path
from uuid import UUID

import uuid
import boto3

from botocore.exceptions import ClientError

from errors import InvalidConfigError, InvalidParamError, FileNotFoundError

class AWSStorage(object):
    
    def __init__(self, config):
        self.config = config

        if self._is_valid_config():
            
            # Create an S3 client
            self.s3 = boto3.resource('s3')
            self.bucket_name = config.BUCKET_NAME

    def get(self, uuid_name):
        
        if not self._is_valid_config():
            raise InvalidConfigError()

        if not self._is_valid_uuid(uuid_name):
            raise InvalidParamError("This is not a UUID value")

        try:
            response = self.s3.Object(self.bucket_name, uuid_name)
            return response.get()['Body'].read()

        except ClientError as e:
            error("[StorageAWS] Error trying read file{0}".format(e))
            raise FileNotFoundError(uuid_name)

    def save(self, raw_file):

        if not self._is_valid_config():
            raise InvalidConfigError()

        if raw_file is None:
            raise InvalidParamError("This is not a data valid")

        #Generate id object
        uuid_name = str(uuid.uuid4())

        #Save raw_file to AWS
        self.s3.Bucket(self.bucket_name).put_object(Key=uuid_name, Body=raw_file)

        return uuid_name

    def remove(self, uuid_name):
        
        if not self._is_valid_config():
            raise InvalidConfigError()

        if not self._is_valid_uuid(uuid_name):
            raise InvalidParamError("This is not a UUID value")

        #Delete from AWS
        try:
            self.s3.Object(self.bucket_name, uuid_name).delete()
        except Exception as e:
            error("[StorageAWS] Error trying read file{0}".format(e))
            return False

        return True

        
    def _is_valid_config(self):
        if self.config is None:
            return False

        if not hasattr(self.config, 'BUCKET_NAME'):
            return False
        else:
            return True
        
    def _is_valid_uuid(self, uuid_name):
        try:
            if UUID(str(uuid_name)).version:
                return True
        except ValueError:
            return False

    def _is_path_exists(self):
        return False
