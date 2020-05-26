
class User:
    def __init__(self, id, pw, name):
        self.id = id
        self.pw = pw
        self.name = name

    def __repr__(self):
        return f'<User: {self.id}>'