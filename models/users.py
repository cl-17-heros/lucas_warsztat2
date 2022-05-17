import hashlib
import datetime
import psycopg2


conn = psycopg2.connect(database='demo_db', user='postgres', password='password', host='localhost', port='5432')
conn.autocommit = True
cursor_ = conn.cursor()


class User:
    def __init__(self, username="", password=""):
        self._id = -1
        self.username = username
        self._hashed_password = hashlib.md5(password.encode()).digest()
        pass

    @property
    def id(self):
        return self._id

    def set_password_hash(self, password):
        self._hashed_password = hashlib.md5(password.encode()).digest()

    @property
    def hashed_password(self):
        return self._hashed_password

    @hashed_password.setter
    def hashed_password(self, value):
        self.set_password_hash(value)

    def save_to_db(self, cursor):
        if self._id == -1:
            u = User()
            check = u.load_all_users(cursor_)
            if self.username not in str(check):
                sql = """INSERT INTO users(username, hashed_password)
                    VALUES (%s, %s) RETURNING id"""
                values = (self.username, self.hashed_password)
                cursor.execute(sql, values)
                self._id = cursor_.fetchone()[0]
                # print(self._id)
                print(f"Inserted user: {self.username} to Database")
            else:
                sql = """UPDATE users SET username = %s, hashed_password = %s
                        WHERE username = %s"""
                values = (self.username, self.hashed_password, self.username)
                cursor.execute(sql, values)
                cursor.close()
                print('Updated database')

    @staticmethod
    def load_user_by_username(cursor, name):
        sql = """SELECT id, username FROM users
                 WHERE username = %s"""
        cursor.execute(sql, (name, ))
        data = cursor.fetchone()
        if data:
            id_, username = data
            loaded_user = User(username)
            loaded_user.username = name
            loaded_user._id = id_
            return loaded_user

    @staticmethod
    def load_user_by_id(cursor, idx):
        sql = """SELECT id, username, hashed_password FROM users 
                 WHERE id = %s"""
        cursor.execute(sql, (idx,))
        data = cursor.fetchone()
        if data:
            idx, username, hashed_password = data
            loaded_user = User(username)
            loaded_user._id = idx
            loaded_user._hashed_password = hashed_password
            return loaded_user
        else:
            return None

    # load_user_by_id(cursor_, -1)

    @staticmethod
    def load_all_users(cursor):
        sql = """SELECT id, username, hashed_password FROM users"""
        cursor.execute(sql)
        users = []
        for row in cursor.fetchall():
            idx, username, hashed_password = row
            loaded_user = User(username)
            loaded_user._id = idx
            loaded_user.username = username
            loaded_user._hashed_password = hashed_password
            users.append(loaded_user)
        return users

    def delete(self, cursor):
        sql = """DELETE FROM users WHERE username = %s"""
        cursor.execute(sql, (self.username, ))
        self._id = -1
        return True

    def __str__(self):
        return f'ID: {self.id} username: {self.username}'

    def __repr__(self):
        return f'ID: ({self.id}) Username: {self.username}'
