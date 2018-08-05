from logging import info, error
from os import path
from uuid import UUID
from botocore.exceptions import ClientError
from errors import InvalidConfigError, InvalidParamError, FileNotFoundError, AWSExceptionError

import uuid

class AWSStorage(object):
    """
    AWS S3 storage
    """

    def __init__(self, config):
        self.config = config

        if not self._is_valid_config():
            raise InvalidConfigError()

    def get(self, uuid_name):
        
        if not self._is_valid_uuid(uuid_name):
            raise InvalidParamError("This is not a UUID value")

        try:
            response = self.config.S3.get_object(Bucket=self.config.BUCKET_NAME, Key=uuid_name)
            return response.get()['Body'].read()
        
        except ClientError as e:
            if e.response['Error']['Code'] == 'NoSuchKey':
                error("[StorageAWS] Key not found {0}".format(e))
                raise FileNotFoundError(uuid_name)
            else:
                error("[StorageAWS] Error trying read file{0}".format(e))
                raise Exception()

    def save(self, uuid_name, raw_file):

        if raw_file is None:
            raise InvalidParamError("This is not a data valid")

        if not self._is_valid_uuid(uuid_name):
            raise InvalidParamError("This is not a uuid valid")

        try:
            self.config.S3.put_object(Bucket=self.config.BUCKET_NAME, Key=uuid_name, Body=raw_file)
            return True
        
        except Exception as e:
            error("[StorageAWS] Error trying save file{0}".format(e))
            raise AWSExceptionError("can't save object ")

    def remove(self, uuid_name):
        
        if not self._is_valid_config():
            raise InvalidConfigError()

        if not self._is_valid_uuid(uuid_name):
            raise InvalidParamError("This is not a UUID value")

        try:
            self.config.S3.delete_object(Bucket=self.config.BUCKET_NAME, Key=str(uuid_name))
            return True

        except Exception as e:
            error("[StorageAWS] Error trying remove file{0}".format(e))
            raise AWSExceptionError("can't remove object {0}".format(e))

    
    #Private functions
    def _get_new_uuid(self):
        uuid_name = str(uuid.uuid4())
        return uuid_name
        
    def _is_valid_config(self):
        if self.config is None:
            return False

        if (not hasattr(self.config, 'BUCKET_NAME') or self.config.BUCKET_NAME == ''
            or not  hasattr(self.config, 'KEY') or self.config.KEY == ''
            or not  hasattr(self.config, 'SECRET_KEY') or self.config.SECRET_KEY == ''):
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
