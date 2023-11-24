from flask import Flask
from vote.config import get_config

app = Flask(__name__)
if app.debug is True:
    Config = get_config('development')
    print(Config.connect_string)
    print(Config.voting_credentials)
elif app.testing is True:
    Config = get_config('testing')
else:
    Config = get_config('production')



from vote.routes import *