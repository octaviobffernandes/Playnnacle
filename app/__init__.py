import os
import json
from dotenv import load_dotenv
from pathlib import Path
from flask import Flask, url_for
from mongoengine import connect
from apispec import APISpec
from apispec.ext.flask import FlaskPlugin
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec.utils import validate_swagger
from flask_swagger_ui import get_swaggerui_blueprint
from .instance.config import app_config
from .country_module.resources import CountryResource
from .country_module.schemas import CountrySchema
from .person_module.resources import PeopleResource
from .person_module.schemas import GetPersonSchema, CreatePersonSchema, UpdatePersonSchema
from .person_module.blueprint import person_blueprint, person_view

vars_path = Path('.') / 'vars.env'
private_vars_path = Path('.') / 'private_vars.env'
load_dotenv(dotenv_path=vars_path)
load_dotenv(dotenv_path=private_vars_path)

config_name = os.getenv('APP_SETTINGS')
app = Flask(__name__)
app.config.from_object(app_config[config_name])

spec = APISpec(
    title='Swagger Playnnacle',
    version='1.0.0',
    openapi_version='2.0',
    plugins=[
        FlaskPlugin(),
        MarshmallowPlugin(),
    ],
)

countryresource = CountryResource.as_view('country')
app.add_url_rule('/country/', view_func=countryresource)
app.register_blueprint(person_blueprint)

spec.definition('GetPersonSchema', schema=GetPersonSchema)
spec.definition('CreatePersonSchema', schema=CreatePersonSchema)
spec.definition('UpdatePersonSchema', schema=UpdatePersonSchema)
spec.definition('CountrySchema', schema=CountrySchema)

with app.test_request_context():
    spec.add_path(url_for('person.people'), view=person_view)
    spec.add_path('/country/', view=countryresource)

validate_swagger(spec)
with app.test_request_context():
    api_url = url_for('static', filename='swagger.json') 
with open('app/static/swagger.json', 'w') as outfile:
    json.dump(spec.to_dict(), outfile)

swagger_url = '/api/docs'
swaggerui_blueprint = get_swaggerui_blueprint(swagger_url, api_url, config={'app_name': "Playnnacle"})
app.register_blueprint(swaggerui_blueprint, url_prefix=swagger_url)

connect(host=app_config[config_name].MONGODB_CONNSTR.format(os.getenv('MONGODB_USER'), os.getenv('MONGODB_PASSWORD')))

if __name__ == '__main__':
    app.run()
