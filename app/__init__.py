import os
from dotenv import load_dotenv
from pathlib import Path
from flask import Flask
from mongoengine import connect
from .instance.config import app_config
from .country_module import country_blueprint
from .person_module import person_blueprint
from .instance.swagger import configure_swagger

vars_path = Path('.') / 'vars.env'
private_vars_path = Path('.') / 'private_vars.env'
load_dotenv(dotenv_path=vars_path)
load_dotenv(dotenv_path=private_vars_path)

config_name = os.getenv('APP_SETTINGS')
app = Flask(__name__)
app.config.from_object(app_config[config_name])
app.register_blueprint(person_blueprint)
app.register_blueprint(country_blueprint)

configure_swagger(app)

connect(host=app.config['MONGODB_CONNSTR'].format(os.getenv('MONGODB_USER'), os.getenv('MONGODB_PASSWORD')))

if __name__ == '__main__':
    app.run()


