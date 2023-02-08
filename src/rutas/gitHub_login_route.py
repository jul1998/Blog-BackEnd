import os
from ..main import request, jsonify, app, bcrypt, create_access_token, get_jwt_identity, jwt_required, get_jwt,login_manager
from ..db import db
from ..modelos import User, Comments, Posts
from flask import Flask, url_for, redirect
from datetime import datetime, timezone, time
import json
from ..utils import APIException
import requests

@app.route("/github-auth")
def github_auth():
    CLIEND_ID = os.getenv("GITHUB_CLIENT_ID")
    CLIENT_SECRET = os.getenv("GITHUB_CLIENT_SECRET")
    code = request.args.get("code")
    if not code:
        raise APIException("Missing code parameter", status_code=400)

    headers = {
        "Accept": "application/json"
    }
    data = {
        "client_id": CLIEND_ID,
        "client_secret": CLIENT_SECRET,
        "code": code
    }
    result = requests.post("https://github.com/login/oauth/access_token", headers=headers, data=data)

    if result.status_code != 200:
        raise APIException("Failed to retrieve access token", status_code=500)

    access_token = result.json()["access_token"]

    headers = {
        "Authorization": f"token {access_token}"
    }
    result1 = requests.get("https://api.github.com/user", headers=headers)

    if result1.status_code != 200:
       raise APIException("Failed to retrieve user data", status_code=500)

    user = result1.json()
    print(access_token)

    #access_token = create_access_token(identity=user.id, additional_claims={"is_administrator": False}, fresh=True) # Fresh here means that token whill refresh when user is authenticated
    #return jsonify({"token": access_token, "user_id":user.id , "email": user.email, "message": f"Welcome, {user.name.split(' ')[0]}"}), 200
    # You can now store the user data in your database, or implement a session-based authentication to keep the user logged in
    return jsonify({"message": "Successfully authenticated with GitHub", "token": access_token})