import boto3
import json

ssm = boto3.client('ssm')

class ProductionConfig(object):
    connect_string = ssm.get_parameter(Name='devISSU-admin-connect-string')['Parameter']['Value']
    dbname = 'undlFiles'
    voting_credentials = json.loads(ssm.get_parameter(Name='voting-credentials')['Parameter']['Value'])

class DevConfig(ProductionConfig):
    connect_string = ssm.get_parameter(Name='devISSU-admin-connect-string')['Parameter']['Value']
    dbname = 'dev_undlFiles'

class TestConfig(ProductionConfig):
    
    pass

def get_config(env):
    if env == 'development':
        print("Got dev config")
        return DevConfig
    elif env == 'production':
        print("Got production config")
        return ProductionConfig
    elif env == 'testing':
        print("Got test config")
        return TestConfig