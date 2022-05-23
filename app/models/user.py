from werkzeug.security import generate_password_hash, check_password_hash
from app.models import db, sharedFiles


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(20), nullable=False)
    lastname = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(320), nullable=False, unique=True)
    phone = db.Column(db.String(10), unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)
    role_id = db.Column(db.ForeignKey('role.id',
                                      onupdate='cascade',
                                      ondelete='cascade'),
                        nullable=True)

    member = db.relationship('Member', back_populates='user', uselist=False)
    role = db.relationship('Role', back_populates='users')
    uploadedFiles = db.relationship('File', back_populates='owner')
    recievedFiles = db.relationship('File',
                                    back_populates='audience',
                                    secondary=sharedFiles.sharedFiles)
    # staff or admin approve or decline a membership application
    approvedSubscriptions = db.relationship('Applications',
                                            back_populates='approvee',
                                            lazy='dynamic')
    approvedposts = db.relationship('ForumPost',
                                    back_populates='approvee',
                                    lazy='dynamic')
    events = db.relationship('Event', back_populates='uploader')

    @property
    def hash_password(self):
        self.password = generate_password_hash(self.password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    @classmethod
    def seeders(cls, faker):
        return cls(firstname=faker.first_name(),
                   lastname=faker.last_name(),
                   email=faker.ascii_safe_email(),
                   password=faker.password(),
                   phone=faker.phone_number()[:10])
