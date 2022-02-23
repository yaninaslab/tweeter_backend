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
        email, username, password, bio, birthdate, image_url, banner_url):
    new_user = None
    conn, cursor = connect_db()
    try:
        salt = create_salt()
        cursor.execute(
            "insert into user(email, username, password, bio, birthdate, image_url, banner_url, salt) values(?, ?, ?, ?, ?, ?, ?, ?)", [email, username, password, bio, birthdate, image_url, banner_url, salt])
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


def update_user(new_password, new_bio, new_image_url, user_id):
    success = None
    conn, cursor = connect_db()
    try:
        cursor.execute(
            "update user set password = ?, bio = ?, image_url = ? where id = ?", [new_password, new_bio, new_image_url, user_id])
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


def log_user(login_token):
    login_token = None
    conn, cursor = connect_db()
    try:
        cursor.execute(
            "insert into user_session(login_token) values(?)", [login_token])
        conn.commit()
        if(cursor.rowcount == 1):
            login_token = True
    except db.OperationalError:
        print("Something is wrong with the DB, please try again in 5 minutes")
    except db.ProgrammingError:
        print("Error running DB query, please file bug report")
    except:
        print("Something went wrong!")
    disconnect_db(conn, cursor)
    return login_token
