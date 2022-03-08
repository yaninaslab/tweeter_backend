from email.mime import image
import dbinteractions as dbi
from flask import Flask, request, Response
import json
import hashlib

import sys

app = Flask(__name__)

# Using Flask decorator to define an endpoint


@app.get('/api/users')
# Defining the function
def get_all_users():
    # Actions inside try-except block
    try:
        # Assigning a variable as an output from the function
        users = dbi.get_all_users()
        # Converting data from python to json with json.dumps() method
        users_json = json.dumps(users, default=str)
        # Returning response in json and request status
        return Response(users_json, mimetype="application/json", status=200)
    except:
        # In case of error this will be returned
        print("Something went wrong")
        return Response("Sorry, something is wrong with the service. Please try again later", mimetype="plain/text", status=501)

# Using Flask decorator to define an endpoint


@app.post('/api/users')
def add_new_user():
    try:
        # Requesting data from the frontend
        email = request.json['email']
        username = request.json['username']
        password = request.json['password']
        bio = request.json['bio']
        birthdate = request.json['birthdate']
        # I commented the following two lines because I don't have this functionlity on the frontend.
        # image_url = request.json['image_url']
        # banner_url = request.json['banner_url']
        # Here we are assigning variables that would be returned by a function that takes arguments in the brackets
        new_user, login_token, user_id = dbi.add_new_user(
            email, username, password, bio, birthdate)
        # This is a condition saying that if the function returns a 'new_user' we're accepting it as an object and converting it to json
        if(new_user == True):
            new_user = {
                "userId": user_id,
                "email": email,
                "username": username,
                "bio": bio,
                "bithdate": birthdate,
                # "imageUrl": image_url,
                # "bannerUrl": banner_url,
                "loginToken": login_token
            }
            new_user_json = json.dumps(new_user, default=str)
            # Returning response in json and request status
            return Response(new_user_json, mimetype="application/json", status=200)
        else:
            return Response("Please enter valid data", mimetype="plain/text", status=400)
# In case of error this will be returned
    except:
        print("Something went wrong")
        return Response("Sorry, something is wrong with the service. Please try again later", mimetype="plain/text", status=501)

# Using Flask decorator to define an endpoint


@app.delete('/api/users')
def delete_user():
    try:
        # Requesting data from the frontend
        user_id = request.json['user_id']
        # We assign a variable to the function output and if it's true, we convert the data into json
        user_id = dbi.delete_user(user_id)
        if(user_id == True):
            user_id_json = json.dumps(user_id, default=str)
            # Returning response in json and request status
            return Response(user_id_json, mimetype="application/json", status=200)
        else:
            return Response("Please enter valid data", mimetype="plain/text", status=400)
# In case of error this will be returned
    except:
        print("Something went wrong")
        return Response("Sorry, something is wrong with the service. Please try again later", mimetype="plain/text", status=501)

# Using Flask decorator to define an endpoint


@app.patch('/api/users')
def update_user():
    try:
        # Requesting data from the frontend
        login_token = request.json['loginToken']
        password = request.json['password']
        bio = request.json['bio']
        image_url = request.json['imageUrl']
        # Here we are assigning variables that would be returned by a function that takes arguments in the brackets
        success, user, user_id = dbi.update_user(login_token,
                                                 password, bio, image_url)
        # In case of a success we convert the user into an object and then to json
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
            # Returning response in json and request status
            return Response(user_json, mimetype="application/json", status=200)
        else:
            return Response("Please enter valid data", mimetype="plain/text", status=400)
# In case of error this will be returned
    except:
        print("Something went wrong")
        return Response("Sorry, something is wrong with the service. Please try again later", mimetype="plain/text", status=501)

# Using Flask decorator to define an endpoint


@app.post('/api/login')
def log_user():
    try:
        # Requesting data from the frontend
        email = request.json['email']
        password = request.json['password']
        # Returning values from the function and sql query
        login_token, success, user = dbi.log_user(email, password)
        # In case of a success we convert the user into an object and then to json
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
            # Returning response in json and request status
            return Response(user_json, mimetype="application/json", status=200)
        else:
            return Response("Please enter valid data", mimetype="plain/text", status=400)
# In case of error this will be returned
    except:
        print("Something went wrong")
        return Response("Sorry, something is wrong with the service. Please try again later", mimetype="plain/text", status=501)

# Using Flask decorator to define an endpoint


@app.delete('/api/login')
def logout_user():
    try:
        # Requesting data from the frontend
        login_token = request.json['loginToken']
        # In case of success we're getting 204 status and no data returned
        success = dbi.logout_user(login_token)
        if(success == True):
            return Response(mimetype="application/json", status=204)
        else:
            return Response("Please enter valid data", mimetype="plain/text", status=400)
# In case of error this will be returned
    except:
        print("Something went wrong")
        return Response("Sorry, something is wrong with the service. Please try again later", mimetype="plain/text", status=501)

# Using Flask decorator to define an endpoint


@app.get('/api/follows')
def get_my_follows():
    try:
        # Requesting data from the frontend. We're using args because we need to pass params for GET request
        user_id = request.args['userId']
        # Getting the list of follows that the user(userId) follows
        follows = dbi.get_my_follows(user_id)
        follows_json = json.dumps(follows, default=str)
        # Returning response in json and request status
        return Response(follows_json, mimetype="application/json", status=200)
# In case of error this will be returned
    except:
        print("Something went wrong")
        return Response("Sorry, something is wrong with the service. Please try again later", mimetype="plain/text", status=501)

# Using Flask decorator to define an endpoint


@app.post('/api/follows')
def follow_other_users():
    try:
        # Requesting data from the frontend
        login_token = request.json['loginToken']
        follower_id = request.json['followId']
        success = dbi.follow_other_users(
            login_token, follower_id)
        # On success no data is returned
        if(success == True):
            return Response(mimetype="application/json", status=204)
        else:
            return Response("Please enter valid data", mimetype="plain/text", status=400)

    except:
        print("Something went wrong")
        return Response("Sorry, something is wrong with the service. Please try again later", mimetype="plain/text", status=501)

# Using Flask decorator to define an endpoint


@app.delete('/api/follows')
def unfollow_users():
    try:
        # Requesting data from the frontend
        login_token = request.json['loginToken']
        follower_id = request.json['followId']
        success = dbi.unfollow_users(
            login_token, follower_id)
        # On success no data is returned
        if(success == True):
            return Response(mimetype="application/json", status=204)
        else:
            return Response("Please enter valid data", mimetype="plain/text", status=400)

    except:
        print("Something went wrong")
        return Response("Sorry, something is wrong with the service. Please try again later", mimetype="plain/text", status=501)

# Using Flask decorator to define an endpoint


@app.get('/api/followers')
def get_my_followers():
    try:
        # Requesting data from the frontend. We're using args because we need to pass params for GET request
        user_id = request.args['userId']
        # Getting the list of followers that follow that user(userId)
        followers = dbi.get_my_followers(user_id)
        # Returning response in json and request status
        followers_json = json.dumps(followers, default=str)
        return Response(followers_json, mimetype="application/json", status=200)
        # In case of error this will be returned
    except:
        print("Something went wrong")
        return Response("Sorry, something is wrong with the service. Please try again later", mimetype="plain/text", status=501)


@app.get('/api/tweets')
def get_tweets():
    try:
        # user_id = request.args['userId']
        # Getting the list of tweets that the user(userId) follows
        tweets = dbi.get_tweets()
        # Looping through the array of tweets to access required data being returned
        for i in range(len(tweets)):
            # Array inside another array
            tweets[i] = {
                "tweetId": tweets[i][0],
                "userId": tweets[i][1],
                "username": tweets[i][2],
                "content": tweets[i][3],
                "createdAt": tweets[i][4],
            }
        tweets_json = json.dumps(tweets, default=str)
        # Returning response in json and request status
        return Response(tweets_json, mimetype="application/json", status=200)
    except:
        print("Something went wrong")
        return Response("Sorry, something is wrong with the service. Please try again later", mimetype="plain/text", status=501)


@app.post('/api/tweets')
def post_new_tweet():
    try:
        # Requesting data from the frontend
        login_token = request.json['loginToken']
        content = request.json['content']
        success, new_tweet = dbi.post_new_tweet(
            login_token, content)
        # On success we're returning a new_tweet as an object
        if(success == True):
            new_tweet = {
                "tweetId": new_tweet[0],
                "userId": new_tweet[1],
                "username": new_tweet[2],
                "content": new_tweet[3],
                "createdAt": new_tweet[4],
                "imageUrl": new_tweet[5],
            }
        new_tweet_json = json.dumps(new_tweet, default=str)
        return Response(new_tweet_json, mimetype="application/json", status=200)
    except:
        print("Something went wrong")
        return Response("Sorry, something is wrong with the service. Please try again later", mimetype="plain/text", status=501)


@app.patch('/api/tweets')
def update_tweet():
    try:
        # Requesting data from the frontend
        login_token = request.json['loginToken']
        tweet_id = request.json['tweetId']
        content = request.json['content']
        success, updated_tweet = dbi.update_tweet(
            login_token, tweet_id, content)
        if(success == True):
            # On success we update certain values in an object
            updated_tweet = {
                "tweetId": tweet_id,
                "content": content
            }
            updated_tweet_json = json.dumps(updated_tweet, default=str)
            return Response(updated_tweet_json, mimetype="application/json", status=200)
        else:
            return Response("Please enter valid data", mimetype="plain/text", status=400)
    except:
        print("Something went wrong")
        return Response("Sorry, something is wrong with the service. Please try again later", mimetype="plain/text", status=501)


@app.delete('/api/tweets')
def delete_tweet():
    try:
        # Requesting data from the frontend
        login_token = request.json['loginToken']
        tweet_id = request.json['tweetId']
        success = dbi.delete_tweet(
            login_token, tweet_id)
        # On successful delete no data is being returned
        if(success == True):
            return Response(mimetype="application/json", status=204)
        else:
            return Response("Please enter valid data", mimetype="plain/text", status=400)

    except:
        print("Something went wrong")
        return Response("Sorry, something is wrong with the service. Please try again later", mimetype="plain/text", status=501)


@app.get('/api/tweet-likes')
def get_likes():
    try:
        # Requesting data from the frontend
        tweet_id = request.args['tweetId']
        # Getting tweet likes based on tweetId
        tweet_likes = dbi.get_likes(tweet_id)
        tweet_likes_json = json.dumps(tweet_likes, default=str)
        return Response(tweet_likes_json, mimetype="application/json", status=200)
    except:
        print("Something went wrong")
        return Response("Sorry, something is wrong with the service. Please try again later", mimetype="plain/text", status=501)


@app.post('/api/tweet-likes')
def add_like():
    try:
        # Requesting data from the frontend
        login_token = request.json['loginToken']
        tweet_id = request.json['tweetId']
        success = dbi.add_like(
            login_token, tweet_id)
        # On success like is added and no data is being returned
        if(success == True):
            return Response(mimetype="application/json", status=204)
        else:
            return Response("Please enter valid data", mimetype="plain/text", status=400)

    except:
        print("Something went wrong")
        return Response("Sorry, something is wrong with the service. Please try again later", mimetype="plain/text", status=501)


@app.delete('/api/tweet-likes')
def remove_like():
    try:
        # Requesting data from the frontend
        login_token = request.json['loginToken']
        tweet_id = request.json['tweetId']
        success = dbi.remove_like(
            login_token, tweet_id)
        # On success like is removed and no data is being returned
        if(success == True):
            return Response(mimetype="application/json", status=204)
        else:
            return Response("Please enter valid data", mimetype="plain/text", status=400)

    except:
        print("Something went wrong")
        return Response("Sorry, something is wrong with the service. Please try again later", mimetype="plain/text", status=501)


@app.get('/api/comments')
def get_comments():
    try:
        # tweet_id = request.args['tweetId']
        # Getting a full list of comments if no data is sent as an argument
        comments = dbi.get_comments()
        comments_json = json.dumps(comments, default=str)
        return Response(comments_json, mimetype="application/json", status=200)
    except:
        print("Something went wrong")
        return Response("Sorry, something is wrong with the service. Please try again later", mimetype="plain/text", status=501)


@app.post('/api/comments')
def add_comment():
    try:
        # Requesting data from the frontend
        login_token = request.json['loginToken']
        tweet_id = request.json['tweetId']
        content = request.json['content']
        success, comment = dbi.add_comment(login_token, tweet_id, content)
        # On success we're adding a comment as an object
        if(success == True):
            comment = {
                "commentId": comment[0],
                "tweetId": comment[1],
                "userId": comment[2],
                "username": comment[3],
                "content": comment[4],
                "createdAt": comment[5],
            }
        comment_json = json.dumps(comment, default=str)
        return Response(comment_json, mimetype="application/json", status=200)
    except:
        print("Something went wrong")
        return Response("Sorry, something is wrong with the service. Please try again later", mimetype="plain/text", status=501)


@app.patch('/api/comments')
def edit_comment():
    try:
        # Requesting data from the frontend
        login_token = request.json['loginToken']
        comment_id = request.json['commentId']
        content = request.json['content']
        success, comment = dbi.edit_comment(login_token, comment_id, content)
        # Ediding comment's values
        if(success == True):
            comment = {
                "commentId": comment[0],
                "tweetId": comment[1],
                "userId": comment[2],
                "username": comment[3],
                "content": comment[4],
                "createdAt": comment[5],
            }
        comment_json = json.dumps(comment, default=str)
        return Response(comment_json, mimetype="application/json", status=200)
    except:
        print("Something went wrong")
        return Response("Sorry, something is wrong with the service. Please try again later", mimetype="plain/text", status=501)


@app.delete('/api/comments')
def delete_comment():
    try:
        # Requesting data from the frontend
        login_token = request.json['loginToken']
        comment_id = request.json['commentId']
        success = dbi.delete_comment(
            login_token, comment_id)
        # On successful delete no data is returned
        if(success == True):
            return Response(mimetype="application/json", status=204)
        else:
            return Response("Please enter valid data", mimetype="plain/text", status=400)

    except:
        print("Something went wrong")
        return Response("Sorry, something is wrong with the service. Please try again later", mimetype="plain/text", status=501)


@app.get('/api/comment-likes')
def get_com_likes():
    try:
        # Requesting data from the frontend
        comment_id = request.json['commentId']
        # Getting comment likes based on commentId
        comment_likes = dbi.get_com_likes(comment_id)
        comment_likes_json = json.dumps(comment_likes, default=str)
        return Response(comment_likes_json, mimetype="application/json", status=200)
    except:
        print("Something went wrong")
        return Response("Sorry, something is wrong with the service. Please try again later", mimetype="plain/text", status=501)


@app.post('/api/comment-likes')
def add_com_like():
    try:
        # Requesting data from the frontend
        login_token = request.json['loginToken']
        comment_id = request.json['commentId']
        success = dbi.add_com_like(
            login_token, comment_id)
        # On success like is added and no data is being returned
        if(success == True):
            return Response(mimetype="application/json", status=204)
        else:
            return Response("Please enter valid data", mimetype="plain/text", status=400)

    except:
        print("Something went wrong")
        return Response("Sorry, something is wrong with the service. Please try again later", mimetype="plain/text", status=501)


@app.delete('/api/comment-likes')
def remove_com_like():
    try:
        # Requesting data from the frontend
        login_token = request.json['loginToken']
        comment_id = request.json['commentId']
        success = dbi.remove_com_like(
            login_token, comment_id)
        # On success like is removed and no data is being returned
        if(success == True):
            return Response(mimetype="application/json", status=204)
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
