import os
from ..main import request, jsonify, app, bcrypt, create_access_token, get_jwt_identity, jwt_required, get_jwt
from ..db import db
from ..modelos import User, BlockedList, Posts
from flask import Flask, url_for, redirect
from htmlmin import minify

from datetime import datetime, timezone, time
import json
from ..utils import APIException
from datetime import datetime


@app.route("/create_posts", methods=["GET","POST"])
@jwt_required()
def create_post():
    body = request.get_json()
    print(body)
    now = datetime.now().strftime("%Y-%m-%d")
    post_img = None
    if body["post_img"]:
        post_img = body["post_img"]

    try:
        minified_html = minify(body["content"], remove_empty_space=True)
        print(minified_html)
        new_post = Posts(title=body["title"],post_img=post_img, subtitle=body["subtitle"], content=minified_html, created_at = now, author_id=body["author_id"] )
        db.session.add(new_post)
        db.session.commit()
        return jsonify({"message":"Post was created"})
    except Exception as err:
        raise APIException(f"Something went wrong when creating post: {err}", status_code=400)

   

@app.route("/show_posts")
def show_posts():
    posts = Posts.query.all()
    all_posts_list = list(map(lambda post: post.serialize(), posts))
    return jsonify(all_posts_list)

@app.route("/post/<int:post_id>")
@jwt_required()
def show_post_by_id(post_id):
    
    post = Posts.query.filter_by(id=post_id).first()

    if not post:
        raise APIException("Post does not exist", status_code=400)

    return jsonify(post.serialize())