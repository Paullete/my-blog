import os
class Config:
    '''
    General configuration class
    '''
    QUOTES_URL = 'http://quotes.stormconsultancy.co.uk/random.json'
class ProdConfig(Config):
    '''
    Production  configuration class
    '''
    pass
class DevConfig(Config):
    '''
    Development  configuration class
    '''
    DEBUG = True
config_options = {
    'production' : ProdConfig,
    'development' : DevConfig
}