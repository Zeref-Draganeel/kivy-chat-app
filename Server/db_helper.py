import contextlib
import sqlite3


class con:
    def __init__(self, default_name):
        self.name = default_name

    def __enter__(self, name=None):
        if not name:
            name = self.name
        with contextlib.suppress(Exception): self.conn = sqlite3.connect(name)
        with contextlib.suppress(Exception): self.cur = self.conn.cursor()
        return self

    def __exit__(self, *a, **kw):
        with contextlib.suppress(Exception): self.conn.commit()
        with contextlib.suppress(Exception): self.cur.close()
        with contextlib.suppress(Exception): self.conn.close()

    def execute(self, *a, **kw):
        return self.cur.execute(*a, **kw)


con = con('server.db')
with con as cur:
    cur.execute('''
    CREATE TABLE IF NOT EXISTS Users (
            username TEXT NOT NULL PRIMARY KEY,
            password TEXT NOT NULL
    );
    ''')
    cur.execute('''
    CREATE TABLE IF NOT EXISTS Messages (
            messageid INTEGER PRIMARY KEY AUTOINCREMENT,
            user TEXT,
            message TEXT NOT NULL
    );
    ''')


def add_user(username, password):
    with con as cur:
        cur.execute('''INSERT INTO Users values (?, ?);''', (username, password))


def get_user(username):
    with con as cur:
        return cur.execute("SELECT * FROM Users WHERE username=:username;", {"username": username}).fetchone()


def get_users():
    with con as cur:
        return cur.execute('''SELECT username FROM Users;''').fetchall()


def create_message(user, message):
    with con as cur:
        cur.execute('''INSERT INTO Messages (user, message) values (?, ?);''', (user, message))


def get_message(messageid):
    with con as cur:
        return cur.execute("SELECT * FROM Messages WHERE messageid=:messageid;", {"messageid": messageid}).fetchone()


def get_messages():
    with con as cur:
        return cur.execute("SELECT * FROM Messages ORDER BY messageid DESC LIMIT 10;").fetchall()[::-1]
