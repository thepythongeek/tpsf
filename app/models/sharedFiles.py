from app.models import db

sharedFiles = db.Table(
    'sharedFiles', db.metadata,
    db.Column('files_id',
              db.ForeignKey('file.id', ondelete='cascade', onupdate='cascade'),
              primary_key=True),
    db.Column('user_id',
              db.ForeignKey('user.id', ondelete='cascade', onupdate='cascade'),
              primary_key=True))
