from ..db import db
import os

#create a class for comments using db.Model
class Comments(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, nullable=False)
    comment = db.Column(db.Text, nullable=False)
    comment_author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    comment_author = db.relationship("User", back_populates="comments")

    def serialize(self):
        return ({
            "id": self.id,
            "comment": self.comment,
            "created_at": self.created_at,
            "comment_author_id": self.comment_author_id,
            "comment_author": self.comment_author.serialize()
        })
