from flask import url_for
from app.models import db


class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    description = db.Column(db.Text)
    user_id = db.Column(db.ForeignKey('user.id',
                                      onupdate='cascade',
                                      ondelete='set null'),
                        nullable=True)

    assets = db.relationship('MediaAssets', back_populates='event')
    uploader = db.relationship('User', back_populates='events')

    @property
    def json(self):
        return {
            "id":
            self.id,
            "title":
            self.title,
            "description":
            self.description,
            "assets":
            [url_for('static', filename=asset.name) for asset in self.assets]
        }
