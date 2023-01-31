from ..db import db
import os

class Posts(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    subtitle = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    post_img = db.Column(db.Text(), unique= False, nullable=True)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    author = db.relationship("User", back_populates="post")#References User table
    comments = db.relationship('Comments', backref='posts', lazy=True)

    
    def __repr__(self):
        return '<Post %r>' % self.title

    def serialize(self):
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "author_id": self.author_id,
            "author_name": self.author.name,
            "created_at": self.created_at,
            "subtitle": self.subtitle,
            "post_img": self.post_img,
            "comments": list(map(lambda comment: comment.serialize(), self.comments))
        }