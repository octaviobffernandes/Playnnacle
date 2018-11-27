class PublisherModel:
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "<Publisher: {}>".format(self.name)

    def json(self):
        return {'name': self.name}
