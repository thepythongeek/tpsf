import random
from app.models import db


class Membership(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    registrationFee = db.Column(db.Float)
    subscriptionFee = db.Column(db.Float)
    extraDetails = db.Column(db.Text)
    duration = db.Column(db.Integer)

    subscriptions = db.relationship('Applications', back_populates='membership')

    @classmethod
    def seeder(cls, fake):
       return cls(name=fake.color_name(),
                   registrationFee=random.randint(500, 3000),
                   subscriptionFee=random.randint(500, 3000),
                   extraDetails=fake.paragraph(),
                   duration=random.randint(1, 12))