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
                "imageUrl": image_url,
                "bannerUrl": banner_url,
                "loginToken": login_token
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
        login_token = request.json['loginToken']
        password = request.json['password']
        bio = request.json['bio']
        image_url = request.json['imageUrl']
        success, user, user_id = dbi.update_user(login_token,
                                                 password, bio, image_url)
        if(success == True):
            user = {
                "userId": user_id,
                "email": user[1],
                "username": user[2],
                "bio": user[3],
                "bithdate": user[4],
                "imageUrl": user[5],
                "bannerUrl": user[6],
            }
            user_json = json.dumps(user, default=str)
            return Response(user_json, mimetype="application/json", status=200)
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
        login_token, success, user = dbi.log_user(email, password)
        if(success == True):
            user = {
                "userId": user[0],
                "email": user[1],
                "username": user[2],
                "bio": user[4],
                "imageUrl": user[6],
                "bannerUrl": user[7],
                "birthdate": user[5],
                "loginToken": login_token
            }
            user_json = json.dumps(user, default=str)
            return Response(user_json, mimetype="application/json", status=200)
        else:
            return Response("Please enter valid data", mimetype="plain/text", status=400)

    except:
        print("Something went wrong")
        return Response("Sorry, something is wrong with the service. Please try again later", mimetype="plain/text", status=501)


@app.delete('/api/login')
def logout_user():
    try:
        login_token = request.json['loginToken']
        success = dbi.logout_user(login_token)
        if(success == True):
            return Response(mimetype="application/json", status=204)
        else:
            return Response("Please enter valid data", mimetype="plain/text", status=400)

    except:
        print("Something went wrong")
        return Response("Sorry, something is wrong with the service. Please try again later", mimetype="plain/text", status=501)


@app.get('/api/follows')
def get_my_follows():
    try:
        user_id = request.json['userId']
        follows = dbi.get_my_follows(user_id)
        follows_json = json.dumps(follows, default=str)
        return Response(follows_json, mimetype="application/json", status=200)
    except:
        print("Something went wrong")
        return Response("Sorry, something is wrong with the service. Please try again later", mimetype="plain/text", status=501)


@app.post('/api/follows')
def follow_other_users():
    try:
        login_token = request.json['loginToken']
        follower_id = request.json['followId']
        success = dbi.follow_other_users(
            login_token, follower_id)
        if(success == True):
            return Response(mimetype="application/json", status=204)
        else:
            return Response("Please enter valid data", mimetype="plain/text", status=400)

    except:
        print("Something went wrong")
        return Response("Sorry, something is wrong with the service. Please try again later", mimetype="plain/text", status=501)


@app.delete('/api/follows')
def unfollow_users():
    try:
        login_token = request.json['loginToken']
        follower_id = request.json['followId']
        success = dbi.unfollow_users(
            login_token, follower_id)
        if(success == True):
            return Response(mimetype="application/json", status=204)
        else:
            return Response("Please enter valid data", mimetype="plain/text", status=400)

    except:
        print("Something went wrong")
        return Response("Sorry, something is wrong with the service. Please try again later", mimetype="plain/text", status=501)


@app.get('/api/followers')
def get_my_followers():
    try:
        user_id = request.json['userId']
        followers = dbi.get_my_followers(user_id)
        followers_json = json.dumps(followers, default=str)
        return Response(followers_json, mimetype="application/json", status=200)
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
