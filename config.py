import os


class Config:
    NAME_SERVICE = 'Python Storage Service'

class DevelopmentConfig(Config):
    DEBUG = True

    def __init__(self):
        from decouple import config

        #General Settings
        self.NAME_SERVICE = config('SERVICE_NAME')

        #AWS Storage
        self.BUCKET_NAME = config('BUCKET_NAME')
        self.KEY = config('KEY')
        self.SECRET_KEY = config('SECRET_KEY')

        #FileSystem Storage
        self.LOCAL_STORAGE_LOCATION = config('LOCAL_STORAGE_LOCATION')

        #Use this class
        self.STORAGE_CLASS = config('STORAGE_CLASS')

class TestConfig(Config):
    DEBUG = True
    TESTING = True

    def __init__(self):
        from decouple import config
        BASE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '/test')

        #General Settings
        self.NAME_SERVICE = config('SERVICE_NAME')

        #AWS Storage
        self.BUCKET_NAME = config('BUCKET_NAME')
        self.KEY = config('KEY')
        self.SECRET_KEY = config('SECRET_KEY')

        #FileSystem Storage
        self.LOCAL_STORAGE_LOCATION = config('LOCAL_STORAGE_LOCATION')
    