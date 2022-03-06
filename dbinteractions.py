import mariadb as db
import dbcreds
import secrets


def create_salt():
    return secrets.token_urlsafe(10)


def create_login_token():
    return secrets.token_urlsafe(50)


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
    users = []
    conn, cursor = connect_db()
    try:
        cursor.execute(
            "select id, email, username, bio, birthdate, image_url, banner_url from user")
        users = cursor.fetchall()
    except db.OperationalError:
        print("Something is wrong with the DB, please try again in 5 minutes")
    except db.ProgrammingError:
        print("Error running DB query, please file bug report")
    except:
        print("Something went wrong!")
    disconnect_db(conn, cursor)
    return users


def add_new_user(
        email, username, password, bio, birthdate):
    new_user = None
    conn, cursor = connect_db()
    try:
        salt = create_salt()
        cursor.execute(
            "insert into user(email, username, password, bio, birthdate, salt) values(?, ?, ?, ?, ?, ?)", [email, username, password, bio, birthdate, salt])
        conn.commit()
        if(cursor.rowcount == 1):
            login_token = create_login_token()
            user_id = cursor.lastrowid
            cursor.execute("insert into user_session(login_token, user_id) values(?, ?)", [
                           login_token, user_id])
            conn.commit()
            new_user = True
    except db.OperationalError:
        print("Something is wrong with the DB, please try again in 5 minutes")
    except db.ProgrammingError:
        print("Error running DB query, please file bug report")
    except:
        print("Something went wrong!")
    disconnect_db(conn, cursor)
    return new_user, login_token, user_id


def delete_user(user_id):
    success = None
    conn, cursor = connect_db()
    try:
        cursor.execute(
            "delete from user where id = ?", [user_id])
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


def update_user(login_token, password, bio, image_url):
    success = None
    user = None
    user_id = None
    conn, cursor = connect_db()
    try:
        cursor.execute(
            "select user_id from user_session where login_token = ?", [login_token])
        user = cursor.fetchone()
        user_id = user[0]
        cursor.execute(
            "update user set password = ?, bio = ?, image_url = ? where id = ?", [password, bio, image_url, user_id])
        conn.commit()
        if(cursor.rowcount == 1):
            cursor.execute(
                "select id, email, username, bio, birthdate, image_url, banner_url from user where id = ?", [user_id])
            user = cursor.fetchone()
            success = True
    except db.OperationalError:
        print("Something is wrong with the DB, please try again in 5 minutes")
    except db.ProgrammingError:
        print("Error running DB query, please file bug report")
    except:
        print("Something went wrong!")
    disconnect_db(conn, cursor)
    return success, user, user_id


def log_user(email, password):
    login_token = None
    success = False
    conn, cursor = connect_db()
    try:
        cursor.execute(
            "select id, email, password, username, bio, image_url, banner_url, birthdate from user where email = ? and password = ?", [email, password])
        user = cursor.fetchone()
        if(user):
            login_token = create_login_token()
            cursor.execute("insert into user_session(login_token, user_id) values(?, ?)", [
                login_token, user[0]])
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
    follows = []
    conn, cursor = connect_db()
    try:
        cursor.execute(
            "select u.id, email, username, bio, birthdate, image_url, banner_url from user u inner join follow f on u.id = f.followed_id where f.follower_id = ?", [user_id])
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
    success = False
    user = None
    user_id = None
    conn, cursor = connect_db()
    try:
        cursor.execute(
            "select user_id from user_session where login_token = ?", [login_token])
        user = cursor.fetchone()
        user_id = user[0]
        cursor.execute(
            "INSERT INTO follow(follower_id, followed_id) VALUES(?, ?)", [user_id, follower_id])
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
    success = False
    user = None
    user_id = None
    conn, cursor = connect_db()
    try:
        cursor.execute(
            "select user_id from user_session where login_token = ?", [login_token])
        user = cursor.fetchone()
        user_id = user[0]
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
    followers = []
    conn, cursor = connect_db()
    try:
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
    tweets = []
    conn, cursor = connect_db()
    try:
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
    return tweets


def post_new_tweet(login_token, content):
    new_tweet = None
    success = False
    conn, cursor = connect_db()
    try:
        cursor.execute(
            "select user_id from user_session where login_token = ?", [login_token])
        user = cursor.fetchone()
        user_id = user[0]
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
        cursor.execute(
            "select user_id from user_session where login_token = ?", [login_token])
        user = cursor.fetchone()
        user_id = user[0]
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
        cursor.execute(
            "select user_id from user_session where login_token = ?", [login_token])
        user = cursor.fetchone()
        user_id = user[0]
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


def get_likes():
    tweet_likes = []
    conn, cursor = connect_db()
    try:
        cursor.execute(
            "select tweet_id, user_id, u.username from tweet_like tl inner join `user` u on u.id = tl.user_id")
        tweet_likes = cursor.fetchall()
    except db.OperationalError:
        print("Something is wrong with the DB, please try again in 5 minutes")
    except db.ProgrammingError:
        print("Error running DB query, please file bug report")
    except:
        print("Something went wrong!")
    disconnect_db(conn, cursor)
    return tweet_likes


def add_like(login_token, tweet_id):
    success = False
    user = None
    user_id = None
    conn, cursor = connect_db()
    try:
        cursor.execute(
            "select user_id from user_session where login_token = ?", [login_token])
        user = cursor.fetchone()
        user_id = user[0]
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
        cursor.execute(
            "select user_id from user_session where login_token = ?", [login_token])
        user = cursor.fetchone()
        user_id = user[0]
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
    comments = []
    conn, cursor = connect_db()
    try:
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
        cursor.execute(
            "select user_id from user_session where login_token = ?", [login_token])
        user = cursor.fetchone()
        user_id = user[0]
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
        cursor.execute(
            "select user_id from user_session where login_token = ?", [login_token])
        user = cursor.fetchone()
        user_id = user[0]
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
        cursor.execute(
            "select user_id from user_session where login_token = ?", [login_token])
        user = cursor.fetchone()
        user_id = user[0]
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
    comment_likes = []
    conn, cursor = connect_db()
    try:
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
    return comment_likes


def add_com_like(login_token, comment_id):
    success = False
    user = None
    user_id = None
    conn, cursor = connect_db()
    try:
        cursor.execute(
            "select user_id from user_session where login_token = ?", [login_token])
        user = cursor.fetchone()
        user_id = user[0]
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
        cursor.execute(
            "select user_id from user_session where login_token = ?", [login_token])
        user = cursor.fetchone()
        user_id = user[0]
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
