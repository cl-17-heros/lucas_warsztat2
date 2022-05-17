# Script to create a new Database. If Database already exists, it returns error DuplicateDatabase
import psycopg2
from psycopg2.errors import DuplicateDatabase, DuplicateTable

# Tries to create the database. If the database already exists,
# it catches the error and prints a user-friendly message.
try:
    # creates a connection
    conn = psycopg2.connect(user='postgres', password='password', host='localhost', port='5432')
    conn.autocommit = True
    cursor = conn.cursor()
    try:
        # Tries to create the database. If the database already exists,
        # it catches the error and prints a user-friendly message.
        create_db = """CREATE database demo_db"""
        cursor.execute(create_db)
        print('Success')
    except DuplicateDatabase as err:
        print(f'Connection Failed due to this error: {err}')
    conn.close()
except psycopg2.OperationalError as err:
    print(f'There was an error: {err}')

# Creates new connection to recently made database, so we can add tables.
try:
    conn = psycopg2.connect(database='demo_db', user='postgres', password='password', host='localhost', port='5432')
    conn.autocommit = True
    cursor = conn.cursor()
    try:
        # Creates a table called users and adds 3 columns to that empty table.
        # id as primary key, username and hashed_password. If the table already
        # exists, it will print the error.
        create_table_users = """CREATE table users(
                    id SERIAL PRIMARY KEY,
                    username VARCHAR(255),
                    hashed_password VARCHAR(80)
                    )"""
        cursor.execute(create_table_users)
        print("Table creation success")
    except DuplicateTable as err:
        print(f"Table creation failed due to the following error: {err}")

    try:
        # Below will try to create a new table called messages. If the table
        # already exists, it will print the error.
        create_table_messages = """CREATE table "messages"(
                    id SERIAL PRIMARY KEY,
                    from_id INTEGER,
                    to_id INTEGER,
                    creation_date TIMESTAMP DEFAULT Now(),
                    text VARCHAR(225), 
                    FOREIGN KEY (from_id) REFERENCES users,
                    FOREIGN KEY (to_id) REFERENCES users
                    )"""
        cursor.execute(create_table_messages)
        print("Table creation success")
    except DuplicateTable as err:
        print(f"Table creation failed due to the following error: {err}")
    conn.close()
except psycopg2.OperationalError as err:
    print(f'There was an error: {err}')
