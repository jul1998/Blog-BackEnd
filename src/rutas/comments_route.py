import os
from ..main import request, jsonify, app, bcrypt, create_access_token, get_jwt_identity, jwt_required, get_jwt,login_manager
from ..db import db
from ..modelos import User, Comments
from flask import Flask, url_for, redirect
from datetime import datetime, timezone, time
import json
from ..utils import APIException
from functools import wraps

@app.route("/create_comment", methods=["POST"])
def create_comment():
    body = request.get_json()
    now = datetime.now().strftime("%Y-%m-%d")
    
    try:
        if body is None:
            raise APIException(
                "Body está vacío o email no viene en el body, es inválido", status_code=400)
        if body['comment'] is None or body['comment'] == "":
            raise APIException("Comment is not valid", status_code=400)
        if body['comment_author_id'] is None or body['comment_author_id'] == "":
            raise APIException("Comment author is not valid", status_code=400)

        #if not User.query.get(body['comment_author_id']):
        #    raise APIException("User does not exist", status_code=400)
        
        new_comment = Comments(comment=body['comment'], comment_author_id=body['comment_author_id'], created_at=now)
        db.session.add(new_comment)
        db.session.commit()
        return jsonify({"message":"Comment Created"}), 200

    except Exception as err:
        db.session.rollback()
        print(err)
        raise APIException(f"Error when registering new comment: {err}", status_code=400)