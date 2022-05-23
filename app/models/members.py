import enum
import random
from app.models import db


class CompanyStatus(enum.Enum):
    private = 'private'
    public = 'public'


class Member(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    companyName = db.Column(db.String(100))
    physicalAddress = db.Column(db.String(100))
    telephone = db.Column(db.String(10))
    email = db.Column(db.String(320))
    companyStatus = db.Column(db.Enum(CompanyStatus))
    registrationCertificateNo = db.Column(db.String(100))
    companyDescription = db.Column(db.Text)
    chairpersonName = db.Column(db.String(100))
    chiefexecutiveName = db.Column(db.String(100))
    user_id = db.Column(
        db.ForeignKey('user.id', ondelete='cascade', onupdate='cascade'))

    user = db.relationship('User', back_populates='member')
    subscriptions = db.relationship('Applications',
                                    back_populates='member',
                                    lazy='dynamic')
    posts = db.relationship('ForumPost', back_populates='member')

    @classmethod
    def seeder(cls, faker):
        return cls(companyName=faker.company(),
                   physicalAddress=faker.address(),
                   telephone=faker.phone_number()[:10],
                   email=faker.ascii_safe_email(),
                   companyStatus=random.choice(
                       [CompanyStatus.private, CompanyStatus.public]),
                   registrationCertificateNo=faker.isbn10(),
                   chairpersonName=faker.name(),
                   chiefexecutiveName=faker.name())
