from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()


class Result(db.Model):

    id = db.Column(db.Integer(), primary_key=True)
    location = db.Column(db.Text(), nullable=False)
    weather = db.Column(db.Text(), nullable=False)
    datetime = db.Column(db.DateTime(), nullable=False)

    def to_dict(self):
        return{
            'location': self.first,
            'weather': self.weather,
            'datetime': self.datetime

        }
