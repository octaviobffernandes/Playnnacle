class PlatformModel:
    def __init__(self, name, abbreviation):
        self.name = name
        self.abbreviation = abbreviation

    def __repr__(self):
        return "<Platform: {}>".format(self.name)

    def json(self):
        return {'name': self.name, 'abbreviation': self.abbreviation}
