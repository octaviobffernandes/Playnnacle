from flask_restful import Resource, reqparse
from models.game import GameModel


class Game(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'name',
        type=str,
        required=True,
        help="This field cannot be left blank!"
    )
    parser.add_argument(
        'genre',
        type=str,
        required=True,
        help="This field cannot be left blank!"
    )
    parser.add_argument(
        'year',
        type=str,
        required=True,
        help="This field cannot be left blank!"
    )

    def get(self, name):
        game = GameModel.get(name)
        if game:
            return game.json(), 200
        else:
            return {'message': 'Game not found'}, 404

    def delete(self, name):
        game = GameModel.get(name)
        if game:
            game.delete()
            return "ok", 200
        return {'message': 'Game not found'}, 404

    def put(self):
        return "ok", 200


class Games(Resource):
    def post(self):
        request_data = Game.parser.parse_args()
        if GameModel.get(request_data.name):
            return {'message': "A game with name '{}' already exists."
                               .format(request_data.name)}, 400

        game = GameModel(request_data.name, request_data.genre, request_data.year)

        try:
            game.save()
        except:
            return {'message': 'An error occurred inserting the game.'}, 500

        return game.json(), 201

    def get(self):
        return {'games': [game.json() for game in GameModel.get_all()]}, 200
