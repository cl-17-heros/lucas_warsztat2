import datetime
import psycopg2

conn = psycopg2.connect(database='demo_db', user='postgres', password='password', host='localhost', port='5432')
conn.autocommit = True
cursor_ = conn.cursor()


class Messages:
    def __init__(self, from_id, to_id, text="", creation_date=None):
        self._id = -1
        self.from_id = from_id
        self.to_id = to_id
        self.text = text
        self.creation_date = creation_date

    @property
    def id(self):
        return self._id

    def save_to_db(self, cursor):
        if self._id == -1:
            sql = """INSERT INTO messages(from_id, to_id, text, creation_date)
                VALUES (%s, %s, %s, %s) RETURNING id"""
            self.creation_date = datetime.datetime.now()
            values = (self.from_id, self.to_id, self.text, self.creation_date)
            cursor.execute(sql, values)
            self._id = cursor.fetchone()[0]
            print("Successfully inserted message into database")
            return True
        else:
            sql = """UPDATE messages SET from_id = %s, to_id = %s, text = %s, creation_date = %s
                    WHERE id = %s"""
            self.creation_date = datetime.datetime.now()
            values = (self.from_id, self.to_id, self.text, self.creation_date, self.id)
            cursor.execute(sql, values)
            return True

    @staticmethod
    def load_all_messages(cursor):
        sql = """SELECT from_id, to_id, creation_date, text FROM messages"""
        cursor.execute(sql)
        users = []
        for row in cursor.fetchall():
            from_id, to_id, creation_date, text = row
            loaded_message = Messages(0, 0)
            loaded_message.from_id = from_id
            loaded_message.to_id = to_id
            loaded_message.creation_date = creation_date
            loaded_message.text = text
            users.append(loaded_message)
        return users

    def __repr__(self):
        return f'From ID: ({self.from_id}) To ID: ({self.to_id}) Message: "{self.text}"'


# m = Messages(15, 16, 'siema')
# m.save_to_db(cursor_)

