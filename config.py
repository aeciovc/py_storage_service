import os


class Config:
    APP_NAME = 'Python Storage Service'

class DevelopmentConfig(Config):
    DEBUG = True

    AWS_KEY = ''
    AWS_SECRET_KEY = ''
    BUCKET_NAME = ''
    S3 = None
    
    def __init__(self):
        from decouple import config

        self.BUCKET_NAME = config('BUCKET_NAME')
        self.KEY = config('KEY')
        self.SECRET_KEY = config('SECRET_KEY')

class TestConfig(Config):
    DEBUG = True
    TESTING = True
    
    AWS_KEY = ''
    AWS_SECRET_KEY = ''
    BUCKET_NAME = ''
    S3 = None

    def __init__(self):
        from decouple import config
        BASE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '/test')

        self.BUCKET_NAME = config('BUCKET_NAME')
        self.KEY = config('KEY')
        self.SECRET_KEY = config('SECRET_KEY')
    