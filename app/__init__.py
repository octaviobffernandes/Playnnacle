import os
import json
from dotenv import load_dotenv
from pathlib import Path
from flask import Flask, url_for
from mongoengine import connect
from apispec import APISpec
from apispec_webframeworks.flask import FlaskPlugin
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec.utils import validate_spec
from flask_swagger_ui import get_swaggerui_blueprint
from .instance.config import app_config
from .country_module import CountryResource, CountrySchema, country_blueprint, country_view
from .person_module import PeopleResource, GetPersonSchema, CreatePersonSchema, UpdatePersonSchema, person_blueprint, person_view, people_view

vars_path = Path('.') / 'vars.env'
private_vars_path = Path('.') / 'private_vars.env'
load_dotenv(dotenv_path=vars_path)
load_dotenv(dotenv_path=private_vars_path)

config_name = os.getenv('APP_SETTINGS')
app = Flask(__name__)
app.config.from_object(app_config[config_name])
app.register_blueprint(person_blueprint)
app.register_blueprint(country_blueprint)

spec = APISpec(
    title='Swagger Playnnacle',
    version='1.0.0',
    openapi_version='2.0',
    plugins=[
        FlaskPlugin(),
        MarshmallowPlugin(),
    ],
)

spec.components.schema('GetPersonSchema', schema=GetPersonSchema)
spec.components.schema('CreatePersonSchema', schema=CreatePersonSchema)
spec.components.schema('UpdatePersonSchema', schema=UpdatePersonSchema)
spec.components.schema('CountrySchema', schema=CountrySchema)

with app.test_request_context():
    spec.path(url_for('person.people'), view=people_view)
    spec.path(url_for('person.person', id=id), view=person_view)
    spec.path(url_for('country.countries'), view=country_view)

validate_spec(spec)
with app.test_request_context():
    api_url = url_for('static', filename='swagger.json') 
with open('app/static/swagger.json', 'w') as outfile:
    json.dump(spec.to_dict(), outfile)

swagger_url = '/api/docs'
swaggerui_blueprint = get_swaggerui_blueprint(swagger_url, api_url, config={'app_name': "Playnnacle"})
app.register_blueprint(swaggerui_blueprint, url_prefix=swagger_url)

connect(host=app.config['MONGODB_CONNSTR'].format(os.getenv('MONGODB_USER'), os.getenv('MONGODB_PASSWORD')))

if __name__ == '__main__':
    app.run()
