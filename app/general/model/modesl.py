from app import db

class Note(db.Model):
    __tablename__ = "note"
    __table_args__ = {'mysql_collate': 'utf8_general_ci'}
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128))
    content = db.Column(db.Text)

    def __init__(self, title, content):
        self.title = title
        self.content = content