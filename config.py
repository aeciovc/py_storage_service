
class Config:
    APP_NAME = 'Python Storage Service'

class DevelopmentConfig(Config):
    DEBUG = True
    
    AWS_KEY = ''
    AWS_SECRET_KEY = ''
    BUCKET_NAME = ''
    S3 = None

class TestConfig(Config):
    DEBUG = True
    TESTING = True
    
    AWS_KEY = ''
    AWS_SECRET_KEY = ''
    BUCKET_NAME = ''
    S3 = None