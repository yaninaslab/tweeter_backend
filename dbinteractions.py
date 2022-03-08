from ast import Assign
import mariadb as db
import dbcreds
import secrets

# Adding salt(extra characters to the password in db)


def create_salt():
    return secrets.token_urlsafe(10)

# Creating login_token for every user session


def create_login_token():
    return secrets.token_urlsafe(50)

# Connecting to db


def connect_db():
    conn = None
    cursor = None
    try:
        conn = db.connect(user=dbcreds.user, password=dbcreds.password,
                          host=dbcreds.host, port=dbcreds.port, database=dbcreds.database)
        cursor = conn.cursor()
    except db.OperationalError:
        print("Something is wrong with the DB, please try again in 5 minutes")
    except:
        print("Something went wrong!")
    return conn, cursor

# Disconnecting from db


def disconnect_db(conn, cursor):
    try:
        cursor.close()
    except:
        print("The issue with cursor")
    try:
        conn.close()
    except:
        print("The issue with connection")


def get_all_users():
    # Assigning an array to accept the results of an SQL query
    users = []
    conn, cursor = connect_db()
    try:
        # Doing SELECT request
        cursor.execute(
            "select id, email, username, bio, birthdate, image_url, banner_url from user")
        # Retrieving data from the database using fetchall(), i.e. all database rows
        users = cursor.fetchall()
        # In case of various errors this will be returned
    except db.OperationalError:
        print("Something is wrong with the DB, please try again in 5 minutes")
    except db.ProgrammingError:
        print("Error running DB query, please file bug report")
    except:
        print("Something went wrong!")
    disconnect_db(conn, cursor)
    # Returning variable from the function
    return users


def add_new_user(
        email, username, password, bio, birthdate):  # Function and its arguments
    # We need to assign a new variable before try-except block if we're going to use it inside the block
    new_user = None
    conn, cursor = connect_db()
    try:
        # Creating salt and adding it to the column in the db
        salt = create_salt()
        # INSERT request with the inputs in []
        cursor.execute(
            "insert into user(email, username, password, bio, birthdate, salt) values(?, ?, ?, ?, ?, ?)", [email, username, password, bio, birthdate, salt])
        conn.commit()
        # The following condition checks if the insert happens
        if(cursor.rowcount == 1):
            # In case the query goes well, login_token is created
            login_token = create_login_token()
            # Assigning value to user_id with lastrowid attribute after the insert took place
            user_id = cursor.lastrowid
            # Another INSERT into user_session table
            cursor.execute("insert into user_session(login_token, user_id) values(?, ?)", [
                           login_token, user_id])
            # Saving changes
            conn.commit()
            # In case sql queries are successful, new_user is set to True and returned to API
            new_user = True
            # In case of various errors this will be returned
    except db.OperationalError:
        print("Something is wrong with the DB, please try again in 5 minutes")
    except db.ProgrammingError:
        print("Error running DB query, please file bug report")
    except:
        print("Something went wrong!")
    disconnect_db(conn, cursor)
    # Returning variables from the function
    return new_user, login_token, user_id


def delete_user(user_id):
    # Assigning a variable to return in the end
    success = None
    conn, cursor = connect_db()
    try:
        # DELETE query based on user_id
        cursor.execute(
            "delete from user where id = ?", [user_id])
        # Saving changes
        conn.commit()
        # The following condition checks if the query happens
        if(cursor.rowcount == 1):
            # In case it does, success is changed to True
            success = True
    except db.OperationalError:
        print("Something is wrong with the DB, please try again in 5 minutes")
    except db.ProgrammingError:
        print("Error running DB query, please file bug report")
    except:
        print("Something went wrong!")
    disconnect_db(conn, cursor)
    return success


def update_user(login_token, password, bio, image_url):  # Function and its arguments
    # Defining variables before try-except block
    success = None
    user = None
    user_id = None
    conn, cursor = connect_db()
    try:
        # SELECT request to pull down login_token from the db
        cursor.execute(
            "select user_id from user_session where login_token = ?", [login_token])
        # Saving this row with fetchone()
        user = cursor.fetchone()
        # Assigning the correct position of user_id in the row 'user'
        user_id = user[0]
        # UPDATE request that's going to edit values
        cursor.execute(
            "update user set password = ?, bio = ?, image_url = ? where id = ?", [password, bio, image_url, user_id])
        # Saving changes
        conn.commit()
        # The following condition checks if the query happens
        if(cursor.rowcount == 1):
            # SELECT query selects the necessary values and returns them as response from db
            cursor.execute(
                "select id, email, username, bio, birthdate, image_url, banner_url from user where id = ?", [user_id])
            # Collecting this data with fetchone()
            user = cursor.fetchone()
            # If the previous line was successful, success is turned to True
            success = True
    except db.OperationalError:
        print("Something is wrong with the DB, please try again in 5 minutes")
    except db.ProgrammingError:
        print("Error running DB query, please file bug report")
    except:
        print("Something went wrong!")
    disconnect_db(conn, cursor)
    # Returning variables from the function
    return success, user, user_id


def log_user(email, password):
    # Defining variables before try-except block
    login_token = None
    success = False
    conn, cursor = connect_db()
    try:
        # SELECT query for gabbing data from user table and compare email and password values
        cursor.execute(
            "select id, email, password, username, bio, image_url, banner_url, birthdate from user where email = ? and password = ?", [email, password])
        # If this combo exists, using fetchone() to store the result in a variable
        user = cursor.fetchone()
        # In case the query is successful, we create a login_token and INSERT it into user_session table for storing this data. user_id is taken from user[0]
        if(user):
            login_token = create_login_token()
            cursor.execute("insert into user_session(login_token, user_id) values(?, ?)", [
                login_token, user[0]])
            # Saving changes
            conn.commit()
            success = True
    except db.OperationalError:
        print("Something is wrong with the DB, please try again in 5 minutes")
    except db.ProgrammingError:
        print("Error running DB query, please file bug report")
    except:
        print("Something went wrong!")
    disconnect_db(conn, cursor)
    return login_token, success, user


def logout_user(login_token):
    success = False
    conn, cursor = connect_db()
    try:
        # To log out, we need to delete login_token from user_session table and we return do data on successful delete
        cursor.execute(
            "delete from user_session where login_token = ?", [login_token])
        conn.commit()
        if(cursor.rowcount == 1):
            success = True
    except db.OperationalError:
        print("Something is wrong with the DB, please try again in 5 minutes")
    except db.ProgrammingError:
        print("Error running DB query, please file bug report")
    except:
        print("Something went wrong!")
    disconnect_db(conn, cursor)
    return success


def get_my_follows(user_id):
    # Defining variables before try-except block
    follows = []
    conn, cursor = connect_db()
    try:
        # Using SELECT statement to retrieve the users that follow the profile with that user_id
        cursor.execute(
            "select u.id, email, username, bio, birthdate, image_url, banner_url from user u inner join follow f on u.id = f.followed_id where f.follower_id = ?", [user_id])
        # Saving data using fetchall()
        follows = cursor.fetchall()
    except db.OperationalError:
        print("Something is wrong with the DB, please try again in 5 minutes")
    except db.ProgrammingError:
        print("Error running DB query, please file bug report")
    except:
        print("Something went wrong!")
    disconnect_db(conn, cursor)
    return follows


def follow_other_users(login_token, follower_id):
    # Defining variables before try-except block
    success = False
    user = None
    user_id = None
    conn, cursor = connect_db()
    try:
        # SELECT request to pull down login_token from the db
        cursor.execute(
            "select user_id from user_session where login_token = ?", [login_token])
        user = cursor.fetchone()
        user_id = user[0]
        # INSERT data into into follow table
        cursor.execute(
            "INSERT INTO follow(follower_id, followed_id) VALUES(?, ?)", [user_id, follower_id])
        # Saving changes
        conn.commit()
        if(cursor.rowcount == 1):
            success = True
    except db.OperationalError:
        print("Something is wrong with the DB, please try again in 5 minutes")
    except db.ProgrammingError:
        print("Error running DB query, please file bug report")
    except:
        print("Something went wrong!")
    disconnect_db(conn, cursor)
    return success


def unfollow_users(login_token, follower_id):
    # Defining variables before try-except block
    success = False
    user = None
    user_id = None
    conn, cursor = connect_db()
    try:
        # SELECT request to pull down login_token from the db
        cursor.execute(
            "select user_id from user_session where login_token = ?", [login_token])
        user = cursor.fetchone()
        user_id = user[0]
        # DELETE request to remove data from follow table, i.e. unfollow a user
        cursor.execute(
            "delete from follow where follower_id = ? and followed_id = ?", [user_id, follower_id])
        conn.commit()
        if(cursor.rowcount == 1):
            success = True
    except db.OperationalError:
        print("Something is wrong with the DB, please try again in 5 minutes")
    except db.ProgrammingError:
        print("Error running DB query, please file bug report")
    except:
        print("Something went wrong!")
    disconnect_db(conn, cursor)
    return success


def get_my_followers(user_id):
    # Define an array to store the results after fetchall()
    followers = []
    conn, cursor = connect_db()
    try:
        # SELECT query for getting data for followers
        cursor.execute(
            "select u.id, email, username, bio, birthdate, image_url, banner_url from user u inner join follow f on u.id = f.follower_id where f.followed_id = ?", [user_id])
        followers = cursor.fetchall()
    except db.OperationalError:
        print("Something is wrong with the DB, please try again in 5 minutes")
    except db.ProgrammingError:
        print("Error running DB query, please file bug report")
    except:
        print("Something went wrong!")
    disconnect_db(conn, cursor)
    return followers


def get_tweets():
    # Define an array to store the results after fetchall()
    tweets = []
    conn, cursor = connect_db()
    try:
        # SELECT query for getting data for all tweets
        cursor.execute(
            "select t.id, t.user_id, u.username, t.content, t.created_at from `user` u inner join tweet t on u.id = t.user_id")
        tweets = cursor.fetchall()
    except db.OperationalError:
        print("Something is wrong with the DB, please try again in 5 minutes")
    except db.ProgrammingError:
        print("Error running DB query, please file bug report")
    except:
        print("Something went wrong!")
    disconnect_db(conn, cursor)
    # Returning the array of tweets
    return tweets


def post_new_tweet(login_token, content):
    new_tweet = None
    success = False
    conn, cursor = connect_db()
    try:
        # SELECT request to pull down login_token from the db
        cursor.execute(
            "select user_id from user_session where login_token = ?", [login_token])
        user = cursor.fetchone()
        user_id = user[0]
        # INSERT new tweet into tweet table based on user_id
        cursor.execute(
            "INSERT INTO tweet(content, user_id) VALUES(?, ?)", [content, user_id])
        conn.commit()
        if(cursor.rowcount == 1):
            success = True
        cursor.execute(
            "select t.id, t.user_id, u.username, t.content, t.created_at, u.image_url from `user` u inner join tweet t on u.id = t.user_id where t.user_id = ?", [user_id])
        new_tweet = cursor.fetchone()
    except db.OperationalError:
        print("Something is wrong with the DB, please try again in 5 minutes")
    except db.ProgrammingError:
        print("Error running DB query, please file bug report")
    except:
        print("Something went wrong!")
    disconnect_db(conn, cursor)
    return success, new_tweet


def update_tweet(login_token, tweet_id, content):
    updated_tweet = None
    success = False
    conn, cursor = connect_db()
    try:
        # SELECT request to pull down login_token from the db
        cursor.execute(
            "select user_id from user_session where login_token = ?", [login_token])
        user = cursor.fetchone()
        user_id = user[0]
        # UPDATE columns in tweet based on tweet_id
        cursor.execute(
            "update tweet set content = ? where id = ?", [content, tweet_id])
        conn.commit()
        if(cursor.rowcount == 1):
            success = True
        cursor.execute(
            "select t.id, t.content from tweet where t.user_id = ?", [user_id])
        updated_tweet = cursor.fetchone()
    except db.OperationalError:
        print("Something is wrong with the DB, please try again in 5 minutes")
    except db.ProgrammingError:
        print("Error running DB query, please file bug report")
    except:
        print("Something went wrong!")
    disconnect_db(conn, cursor)
    return success, updated_tweet


def delete_tweet(login_token, tweet_id):
    success = False
    user = None
    user_id = None
    conn, cursor = connect_db()
    try:
        # SELECT request to pull down login_token from the db
        cursor.execute(
            "select user_id from user_session where login_token = ?", [login_token])
        user = cursor.fetchone()
        user_id = user[0]
        # DELETE a tweet from a table based on user_id
        cursor.execute(
            "delete from tweet where user_id = ? and id = ?", [user_id, tweet_id])
        conn.commit()
        if(cursor.rowcount == 1):
            success = True
    except db.OperationalError:
        print("Something is wrong with the DB, please try again in 5 minutes")
    except db.ProgrammingError:
        print("Error running DB query, please file bug report")
    except:
        print("Something went wrong!")
    disconnect_db(conn, cursor)
    return success


def get_likes(tweet_id):
    # Define an array to store the results after fetchall()
    tweet_likes = []
    conn, cursor = connect_db()
    try:
        # SELECT query for getting data for tweet likes based on tweet_id
        cursor.execute(
            "select tweet_id, user_id, u.username from tweet_like tl inner join `user` u on u.id = tl.user_id where tl.tweet_id = ?", [tweet_id])
        tweet_likes = cursor.fetchall()
    except db.OperationalError:
        print("Something is wrong with the DB, please try again in 5 minutes")
    except db.ProgrammingError:
        print("Error running DB query, please file bug report")
    except:
        print("Something went wrong!")
    disconnect_db(conn, cursor)
    # Returning the array of tweets likes
    return tweet_likes


def add_like(login_token, tweet_id):
    success = False
    user = None
    user_id = None
    conn, cursor = connect_db()
    try:
        # SELECT request to pull down login_token from the db
        cursor.execute(
            "select user_id from user_session where login_token = ?", [login_token])
        user = cursor.fetchone()
        user_id = user[0]
        # INSERT values into tl table based on user_id
        cursor.execute(
            "INSERT INTO tweet_like(user_id, tweet_id) VALUES(?, ?)", [user_id, tweet_id])
        conn.commit()
        if(cursor.rowcount == 1):
            success = True
    except db.OperationalError:
        print("Something is wrong with the DB, please try again in 5 minutes")
    except db.ProgrammingError:
        print("Error running DB query, please file bug report")
    except:
        print("Something went wrong!")
    disconnect_db(conn, cursor)
    return success


def remove_like(login_token, tweet_id):
    success = False
    user = None
    user_id = None
    conn, cursor = connect_db()
    try:
        # SELECT request to pull down login_token from the db
        cursor.execute(
            "select user_id from user_session where login_token = ?", [login_token])
        user = cursor.fetchone()
        user_id = user[0]
        # DELETE data from tl table based on user_id
        cursor.execute(
            "delete from tweet_like where user_id = ? and tweet_id = ?", [user_id, tweet_id])
        conn.commit()
        if(cursor.rowcount == 1):
            success = True
    except db.OperationalError:
        print("Something is wrong with the DB, please try again in 5 minutes")
    except db.ProgrammingError:
        print("Error running DB query, please file bug report")
    except:
        print("Something went wrong!")
    disconnect_db(conn, cursor)
    return success


def get_comments():
    # Define an array to store the results after fetchall()
    comments = []
    conn, cursor = connect_db()
    try:
        # SELECT query for getting data for all comments
        cursor.execute(
            "select c.id, tweet_id, user_id, u.username, content, created_at from comment c inner join `user` u on u.id = c.user_id")
        comments = cursor.fetchall()
    except db.OperationalError:
        print("Something is wrong with the DB, please try again in 5 minutes")
    except db.ProgrammingError:
        print("Error running DB query, please file bug report")
    except:
        print("Something went wrong!")
    disconnect_db(conn, cursor)
    return comments


def add_comment(login_token, tweet_id, content):
    comment = None
    success = False
    conn, cursor = connect_db()
    try:
        # SELECT request to pull down login_token from the db
        cursor.execute(
            "select user_id from user_session where login_token = ?", [login_token])
        user = cursor.fetchone()
        user_id = user[0]
        # INSERT into comment table
        cursor.execute(
            "INSERT INTO comment(content, user_id, tweet_id) VALUES(?, ?, ?)", [content, user_id, tweet_id])
        conn.commit()
        if(cursor.rowcount == 1):
            success = True
        cursor.execute(
            "select c.id, c.tweet_id, c.user_id, u.username, c.content, c.created_at from `user` u inner join comment c on u.id = c.user_id where c.user_id = ?", [user_id])
        comment = cursor.fetchone()
    except db.OperationalError:
        print("Something is wrong with the DB, please try again in 5 minutes")
    except db.ProgrammingError:
        print("Error running DB query, please file bug report")
    except:
        print("Something went wrong!")
    disconnect_db(conn, cursor)
    return success, comment


def edit_comment(login_token, comment_id, content):
    comment = None
    success = False
    conn, cursor = connect_db()
    try:
        # SELECT request to pull down login_token from the db
        cursor.execute(
            "select user_id from user_session where login_token = ?", [login_token])
        user = cursor.fetchone()
        user_id = user[0]
        # UPDATE request setting new values for comment based on its id
        cursor.execute(
            "update comment set content = ? where id = ?", [content, comment_id])
        conn.commit()
        if(cursor.rowcount == 1):
            success = True
        cursor.execute(
            "select c.id, c.tweet_id, c.user_id, u.username, c.content, c.created_at from `user` u inner join comment c on u.id = c.user_id where c.user_id = ?", [user_id])
        comment = cursor.fetchone()
    except db.OperationalError:
        print("Something is wrong with the DB, please try again in 5 minutes")
    except db.ProgrammingError:
        print("Error running DB query, please file bug report")
    except:
        print("Something went wrong!")
    disconnect_db(conn, cursor)
    return success, comment


def delete_comment(login_token, comment_id):
    success = False
    user = None
    user_id = None
    conn, cursor = connect_db()
    try:
        # SELECT request to pull down login_token from the db
        cursor.execute(
            "select user_id from user_session where login_token = ?", [login_token])
        user = cursor.fetchone()
        user_id = user[0]
        # DELETE from comment based on user_id
        cursor.execute(
            "delete from comment where user_id = ? and id = ?", [user_id, comment_id])
        conn.commit()
        if(cursor.rowcount == 1):
            success = True
    except db.OperationalError:
        print("Something is wrong with the DB, please try again in 5 minutes")
    except db.ProgrammingError:
        print("Error running DB query, please file bug report")
    except:
        print("Something went wrong!")
    disconnect_db(conn, cursor)
    return success


def get_com_likes(comment_id):
    # Define an array to store the results after fetchall()
    comment_likes = []
    conn, cursor = connect_db()
    try:
        # SELECT query for getting data for comment likes based on comment_id
        cursor.execute(
            "select comment_id, user_id, u.username from comment_like cl inner join `user` u on u.id = cl.user_id where cl.comment_id = ?", [comment_id])
        comment_likes = cursor.fetchall()
    except db.OperationalError:
        print("Something is wrong with the DB, please try again in 5 minutes")
    except db.ProgrammingError:
        print("Error running DB query, please file bug report")
    except:
        print("Something went wrong!")
    disconnect_db(conn, cursor)
    # Returning the array of tweets likes
    return comment_likes


def add_com_like(login_token, comment_id):
    success = False
    user = None
    user_id = None
    conn, cursor = connect_db()
    try:
        # SELECT request to pull down login_token from the db
        cursor.execute(
            "select user_id from user_session where login_token = ?", [login_token])
        user = cursor.fetchone()
        user_id = user[0]
        # INSERT into cl based on user_id
        cursor.execute(
            "INSERT INTO comment_like(user_id, comment_id) VALUES(?, ?)", [user_id, comment_id])
        conn.commit()
        if(cursor.rowcount == 1):
            success = True
    except db.OperationalError:
        print("Something is wrong with the DB, please try again in 5 minutes")
    except db.ProgrammingError:
        print("Error running DB query, please file bug report")
    except:
        print("Something went wrong!")
    disconnect_db(conn, cursor)
    return success


def remove_com_like(login_token, comment_id):
    success = False
    user = None
    user_id = None
    conn, cursor = connect_db()
    try:
        # SELECT request to pull down login_token from the db
        cursor.execute(
            "select user_id from user_session where login_token = ?", [login_token])
        user = cursor.fetchone()
        user_id = user[0]
        # DELETE from cl based on user_id
        cursor.execute(
            "delete from comment_like where user_id = ? and comment_id = ?", [user_id, comment_id])
        conn.commit()
        if(cursor.rowcount == 1):
            success = True
    except db.OperationalError:
        print("Something is wrong with the DB, please try again in 5 minutes")
    except db.ProgrammingError:
        print("Error running DB query, please file bug report")
    except:
        print("Something went wrong!")
    disconnect_db(conn, cursor)
    return success
