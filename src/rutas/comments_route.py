import os
from ..main import request, jsonify, app, bcrypt, create_access_token, get_jwt_identity, jwt_required, get_jwt,login_manager
from ..db import db
from ..modelos import User, Comments, Posts
from flask import Flask, url_for, redirect
from datetime import datetime, timezone, time
import json
from ..utils import APIException
from functools import wraps

@app.route("/create_comment", methods=["POST"])
def create_comment():
    body = request.get_json()
    now = datetime.now().strftime("%Y-%m-%d")
    
    
    if body is None:
        raise APIException(
            "Body está vacío o email no viene en el body, es inválido", status_code=400)
    if body['comment'] is None or body['comment'] == "":
        raise APIException("Comment is not valid", status_code=400)
    if body['comment_author_id'] is None or body['comment_author_id'] == "":
        raise APIException("Comment author is not valid", status_code=400)
    if body['post_id'] is None or body['post_id'] == "":
        raise APIException("Post id is not valid", status_code=400)
    if not Posts.query.get(body['post_id']):
        raise APIException("Post does not exist", status_code=400) 

    user = User.query.filter_by(id=body['comment_author_id']).first()
    if not user:
        raise APIException("User does not exist", status_code=400)

    try:
        
        new_comment = Comments(comment=body['comment'], post_id=body["post_id"], comment_author_id=body['comment_author_id'], created_at=now)
        db.session.add(new_comment)
        db.session.commit()
        return jsonify({"message":"Comment Created"}), 200

    except Exception as err:
        db.session.rollback()
        print(err)
        raise APIException(f"Error when registering new comment: {err}", status_code=400)

@app.route("/get_comments", methods=["GET"])
def get_comments():
    comments = Comments.query.all()
    comments = list(map(lambda x: x.serialize(), comments))
    return jsonify(comments), 200

@app.route("/display_commnent/comment_id/<int:comment_id>", methods=["GET"])
def display_comment_by_id(comment_id):
    comment = Comments.query.get(comment_id)
    if comment is None:
        raise APIException("Comment not found", status_code=404)
    return jsonify(comment.serialize()), 200

@app.route("/display_all_commnents/post_id/<int:post_id>", methods=["GET"])
def display_all_comments_by_post(post_id):
    comments = Comments.query.filter_by(post_id=post_id).all()
    if comments is None or comments == []:
        raise APIException("Comment not found", status_code=404)
    
    comments_serialized = list(map(lambda comment: comment.serialize(), comments))
    return jsonify(comments_serialized), 200