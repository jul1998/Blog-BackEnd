import os
from ..main import request, jsonify, app, bcrypt, create_access_token, get_jwt_identity, jwt_required, get_jwt
from ..db import db
from ..modelos import User, BlockedList
from flask import Flask, url_for, redirect
from datetime import datetime, timezone, time
import json
from ..utils import APIException


@app.route('/signup', methods=['POST'])
def signup():
    body = request.get_json()
    try:
        if body is None:
            raise APIException(
                "Body está vacío o email no viene en el body, es inválido", status_code=400)
        if body['email'] is None or body['email'] == "":
            raise APIException("Email is not valid", status_code=400)
        if body['password'] is None or body['password'] == "":
            raise APIException("Password is not valid", status_code=400)
        if body['name'] is None or body['name'] == "":
            raise APIException("Name is not valid", status_code=400)
        

        password = bcrypt.generate_password_hash(
            body['password'], 10).decode("utf-8")

        new_user = User(email=body['email'], password=password, is_active=True, name=body['name'], img_profile=None)

        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message":"User Created"}), 200

    except Exception as err:
        db.session.rollback()
        user = User.query.filter_by(email=body['email'])
        if user:
            raise APIException("User already exists", status_code=400)
        print(err)
        raise APIException({"Error when registering new user"}, status_code=400)


@app.route('/login', methods=['POST'])
def login():
    body = request.get_json()
    email = body['email']
    password = body['password']

    user = User.query.filter_by(email=email).first()

    if user is None:
        raise APIException("usuario no existe", status_code=401)

    # validamos el password si el usuario existe y si coincide con el de la BD
    if not bcrypt.check_password_hash(user.password, password):
        raise APIException("usuario o password no coinciden", status_code=401)

    access_token = create_access_token(identity=user.id, additional_claims={"is_administrator": False}, fresh=True) # Fresh here means that token whill refresh when user is authenticated
    return jsonify({"token": access_token, "user_id":user.id , "email": user.email, "message": f"Welcome, {user.name.split(' ')[0]}"}), 200
