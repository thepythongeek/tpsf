import datetime
from app.models import db


class ForumPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    body = db.Column(db.Text)
    postedAt = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    user_id = db.Column(db.ForeignKey('user.id', onupdate='cascade', ondelete='set null'), nullable=True)
    member_id = db.Column(db.ForeignKey('member.id', onupdate='cascade', ondelete='cascade'))
    topic_id = db.Column(db.ForeignKey('forum_topic.id', onupdate='cascade', ondelete='cascade'))

    approvee = db.relationship('User', back_populates='approvedposts')
    member = db.relationship('Member', back_populates='posts')
    topic = db.relationship('ForumTopic', back_populates='posts')
    assets = db.relationship('MediaAssets', back_populates='post')