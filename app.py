import dbinteractions as dbi
from flask import Flask, request, Response
import json
import hashlib

import sys

app = Flask(__name__)


@app.get('/api/users')
def get_all_users():
    try:
        users = dbi.get_all_users()
        users_json = json.dumps(users, default=str)
        return Response(users_json, mimetype="application/json", status=200)
    except:
        print("Something went wrong")
        return Response("Sorry, something is wrong with the service. Please try again later", mimetype="plain/text", status=501)


@app.post('/api/users')
def add_new_user():
    try:
        email = request.json['email']
        username = request.json['username']
        password = request.json['password']
        bio = request.json['bio']
        birthdate = request.json['birthdate']
        image_url = request.json['image_url']
        banner_url = request.json['banner_url']
        new_user, login_token, user_id = dbi.add_new_user(
            email, username, password, bio, birthdate, image_url, banner_url)
        if(new_user == True):
            new_user = {
                "userId": user_id,
                "email": email,
                "username": username,
                "bio": bio,
                "bithdate": birthdate,
                "image_url": image_url,
                "banner_url": banner_url,
                "login_token": login_token
            }
            new_user_json = json.dumps(new_user, default=str)
            return Response(new_user_json, mimetype="application/json", status=200)
        else:
            return Response("Please enter valid data", mimetype="plain/text", status=400)

    except:
        print("Something went wrong")
        return Response("Sorry, something is wrong with the service. Please try again later", mimetype="plain/text", status=501)


@app.delete('/api/users')
def delete_user():
    try:
        user_id = request.json['user_id']
        user_id = dbi.delete_user(user_id)
        if(user_id == True):
            user_id_json = json.dumps(user_id, default=str)
            return Response(user_id_json, mimetype="application/json", status=200)
        else:
            return Response("Please enter valid data", mimetype="plain/text", status=400)

    except:
        print("Something went wrong")
        return Response("Sorry, something is wrong with the service. Please try again later", mimetype="plain/text", status=501)


@app.patch('/api/users')
def update_user():
    try:
        new_password = request.json['password']
        new_bio = request.json['bio']
        new_image_url = request.json['image_url']
        user_id = request.json['user_id']
        user_id = dbi.update_user(
            new_password, new_bio, new_image_url, user_id,)
        if(user_id == True):
            user_id_json = json.dumps(user_id, default=str)
            return Response(user_id_json, mimetype="application/json", status=200)
        else:
            return Response("Please enter valid data", mimetype="plain/text", status=400)
    except:
        print("Something went wrong")
        return Response("Sorry, something is wrong with the service. Please try again later", mimetype="plain/text", status=501)


@app.post('/api/login')
def log_user():
    try:
        email = request.json['email']
        password = request.json['password']
        # salt = dbi.create_salt()
        # password = salt + password
        # hash_result = hashlib.sha512(password.encode()).hexdigest()
        # if(hash_result == login_token):
        login_token = dbi.log_user(email, password)
        if(login_token == True):
            # log_user()
            login_token_json = json.dumps(login_token, default=str)
            return Response(login_token_json, mimetype="application/json", status=200)
        else:
            return Response("Please enter valid data", mimetype="plain/text", status=400)

    except:
        print("Something went wrong")
        return Response("Sorry, something is wrong with the service. Please try again later", mimetype="plain/text", status=501)


if(len(sys.argv) > 1):
    mode = sys.argv[1]
else:
    print("You must pass a mode to run this python script. Either testing or production")
    exit()

if(mode == "testing"):
    print("Running in testing mode")
    from flask_cors import CORS
    CORS(app)
    app.run(debug=True)
elif(mode == "production"):
    print("Running in production mode")
    import bjoern  # type: ignore
    bjoern.run(app, "0.0.0.0", 5006)
else:
    print("Please run with either testing or production. Example:")
    print("python3.10 app.py production")
