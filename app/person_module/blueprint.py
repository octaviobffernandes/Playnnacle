from flask import Blueprint
from . import PeopleResource

person_blueprint = Blueprint('person', __name__, url_prefix='/people')
person_view = PeopleResource.as_view('people')

person_blueprint.add_url_rule('/', view_func=person_view)