from flask_api import FlaskAPI
from flask import request, jsonify, abort
from instance.config import app_config
from app.models import Game


def create_app(config_name):
    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    # app.config.from_pyfile('config.py')

    # TODO: Move code below to a proper class (a controller class or whatever it is called in python)
    @app.route('/games/', methods=['POST', 'GET'])
    def games():
        if request.method == "POST":
            name = str(request.data.get('name', ''))
            genre = str(request.data.get('genre', ''))
            year = str(request.data.get('year', ''))
            if name:
                game = Game(name=name, genre=genre, year=year)
                game.save()
                response = jsonify({
                    'name': game.name,
                    'genre': game.genre,
                    'year': game.year,
                    'date_modified': game.date_modified
                })
                response.status_code = 201
                return response
        else:
            # GET
            # TODO: accept also urls in format games/[name] instead of querystring
            name = str(request.args.get('name', ''))
            game = Game.get(name)
            results = []
            status_code = 200
            if game is not None:
                obj = {
                    'name': game.name,
                    'genre': game.genre,
                    'year': game.year,
                    'date_modified': game.date_modified
                }
                results.append(obj)
            else:
                status_code = 404

            response = jsonify(results)
            response.status_code = status_code
            return response
    return app
