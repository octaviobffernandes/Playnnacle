from flask import Blueprint
from . import PeopleResource, PersonResource

person_blueprint = Blueprint('person', __name__, url_prefix='/people')
people_view = PeopleResource.as_view('people')
person_view = PersonResource.as_view('person')

person_blueprint.add_url_rule('/', view_func=people_view)
person_blueprint.add_url_rule('/<id>', view_func=person_view)
