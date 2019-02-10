import json
from apispec import APISpec
from apispec_webframeworks.flask import FlaskPlugin
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec.utils import validate_spec
from flask import url_for
from flask_swagger_ui import get_swaggerui_blueprint
from app.country_module import CountryResource, CountrySchema , country_view
from app.person_module import PeopleResource, GetPersonSchema, CreatePersonSchema, UpdatePersonSchema, person_view, people_view


def configure_swagger(app):
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
        