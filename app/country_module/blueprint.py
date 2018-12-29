from flask import Blueprint
from . import CountryResource

country_blueprint = Blueprint('country', __name__, url_prefix='/country')
country_view = CountryResource.as_view('countries')

country_blueprint.add_url_rule('/', view_func=country_view)