class DeveloperModel:
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "<Developer: {}>".format(self.name)

    def json(self):
        return {'name': self.name}
