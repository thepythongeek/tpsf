from app.models import db


class MediaAssets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))

    post_id = db.Column(db.ForeignKey('forum_post.id', onupdate='cascade', ondelete='cascade'))
    event_id = db.Column(db.ForeignKey('event.id', onupdate='cascade', ondelete='cascade'))

    post = db.relationship('ForumPost', back_populates='assets')
    event = db.relationship('Event', back_populates='assets')
