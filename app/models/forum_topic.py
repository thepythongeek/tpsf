from app.models import db


class ForumTopic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))

    posts = db.relationship('ForumPost', back_populates='topic')