import random
from app.models import db


class Applications(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float)
    expiresAt = db.Column(db.DateTime)
    isActive = db.Column(db.Boolean)
    member_id = db.Column(db.ForeignKey('member.id',
                                        ondelete='set null',
                                        onupdate='cascade'),
                          nullable=True)
    user_id = db.Column(db.ForeignKey('user.id',
                                      ondelete='set null',
                                      onupdate='cascade'),
                        nullable=True)
    membership_id = db.Column(db.ForeignKey('membership.id',
                                            ondelete='set null',
                                            onupdate='set null'),
                              nullable=True)

    member = db.relationship('Member', back_populates='subscriptions')
    approvee = db.relationship('User', back_populates='approvedSubscriptions')
    membership = db.relationship('Membership', back_populates='subscriptions')

    @classmethod
    def seeders(cls, faker):
        return cls(amount=random.randint(1500, 3000),
                   expiresAt=faker.date_time(),
                   isActive=faker.boolean())
