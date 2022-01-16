import sqlite3
from flask import g

DATABASE = 'db/db'


class DBConnection(object):
    connection = None

    def query_db(cls, query, args=(), one=False):
        cur = cls.get_connection().execute(query, args)
        rv = cur.fetchall()
        cur.close()
        if one:
            if len(rv) > 0:
                return rv[0]
            else:
                return None
        else:
            return rv

    @classmethod
    def get_connection(cls, new=False):
        """Creates return new Singleton database connection"""
        if new or not cls.connection:
            print("Initialized connection...")
            cls.connection = sqlite3.connect(DATABASE, check_same_thread=False)
            cls.connection.row_factory = sqlite3.Row
        return cls.connection

    def get_all_users(cls):
        return [user['username'] for user in cls.query_db('select * from users')]

    def get_user_by_username(cls, username):
        return cls.query_db('SELECT * FROM users where username = ?', (username,), True)

    def get_all_users2(cls):
        return [user['username'] for user in cls.query_db('select * from users')]
