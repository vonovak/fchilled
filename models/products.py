from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False)
    count = db.Column(db.Float, unique=False)

    def __init__(self, name, count = 0):
        self.name = name
        self.count = count