from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tag = db.Column(db.String(80), unique=True)
    name = db.Column(db.String(80), unique=False)
    count = db.Column(db.Float, unique=False)

    def __init__(self, tag, name, count = 0):
        self.tag = tag
        self.name = name
        self.count = count

    def add(self, count):
        self.count += count
        db.session.commit()
        print "add " + self.tag

    def remove(self, count):
        self.count -= count
        db.session.commit()
        print "remove" + self.tag