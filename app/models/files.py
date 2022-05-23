from app.models import db, sharedFiles


class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    user_id = db.Column(db.ForeignKey('user.id',
                                      ondelete='set null',
                                      onupdate='cascade'),
                        nullable=True)

    owner = db.relationship('User', back_populates='uploadedFiles')
    audience = db.relationship('User',
                               back_populates='recievedFiles',
                               secondary=sharedFiles.sharedFiles)
