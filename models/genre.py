class GenreModel:
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "<Genre: {}>".format(self.name)

    def json(self):
        return {'name': self.name}
