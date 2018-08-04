import boto3

class Config:
    APP_NAME = 'Python Storage Service'

class DevelopmentConfig(Config):
    DEBUG = True
    
    AWS_KEY = ''
    AWS_SECRET_KEY = ''
    BUCKET_NAME = ''
    S3 = None

    def load(self):

        # Create an S3 client
        self.S3_CLIENT = boto3.client(
                's3',
                aws_access_key_id = self.AWS_KEY,
                aws_secret_access_key = self.AWS_SECRET_KEY.SECRET_KEY)

class TestConfig(Config):
    DEBUG = True
    TESTING = True
    
    AWS_KEY = ''
    AWS_SECRET_KEY = ''
    BUCKET_NAME = ''
    S3 = None