import os


# parent Config class contains configurations that are used in both production and development stages.
class Config:
    '''
    General configuration parent class
    '''

    QUOTE_API_URL = 'http://quotes.stormconsultancy.co.uk/random.json'


# ProdConfig subclass contains configurations that are used in production stages of our application and inherits from the parent Config class.
class ProdConfig(Config):
    '''
    Production  configuration child class
    Args:
        Config: The parent configuration class with General configuration settings
    '''
    pass


# DevConfig subclass contains configurations that are used in development stages of our application and inherits from the parent Config class.
class DevConfig(Config):
    '''
    Development  configuration child class
    Args:
        Config: The parent configuration class with General configuration settings
    '''

    DEBUG = True


config_options = {
    'development': DevConfig,
    'production': ProdConfig
}