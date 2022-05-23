import enum
from app.models import db


class Roles(enum.Enum):
    admin = 'admin'
    staff = 'staff'


class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Enum(Roles))

    users = db.relationship('User', back_populates='role')

    @classmethod
    def seeder(cls, role):
        return cls(name=role)