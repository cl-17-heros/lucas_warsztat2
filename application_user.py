from models import User, Messages
import argparse
import psycopg2
from psycopg2.errors import UniqueViolation

conn = psycopg2.connect(database='demo_db', user='postgres', password='password', host='localhost', port='5432')
conn.autocommit = True
cursor_ = conn.cursor()

parse = argparse.ArgumentParser(description="User and Message Application")
parse.add_argument('-u', '--username', metavar='username', help='Username of the user')
parse.add_argument('-p', '--password', help='Password of the user')
parse.add_argument('-n', '--new_pass', help='New password for the user')
parse.add_argument('-l', '--list', help='List of users', action='store_true')
parse.add_argument('-d', '--delete', help="Delete a user")
parse.add_argument('-e', '--edit', help="Edit the user")
args = parse.parse_args()

username = args.username
password = args.password
listx = args.list
delete = args.delete
edit = args.edit


def check_user():
    u = User(args.username, args.password)
    x = u.load_user_by_username(cursor_, args.username)
    x = str(x)
    if username in x:
        raise UniqueViolation("User already exists in table")
    else:
        if len(args.password) >= 8:
            u.save_to_db(cursor_)
        else:
            raise ValueError("Password is too short, must be min length of 8")


def edit_password():
    u = User(args.username, args.password)
    x = u.load_user_by_username(cursor_, args.username)
    x = str(x)
    new_pass = args.new_pass
    if args.username not in x:
        raise UniqueViolation("User not found")
    if len(args.password) < 8:
        raise ValueError("Password too short")
    else:
        if len(new_pass) < 8:
            raise ValueError("New password too short. Minimum length of 8")
        else:
            if u._hashed_password == u.hashed_password:
                u._hashed_password = new_pass
            u.save_to_db(cursor_)


def delete_user():
    u = User(args.username, args.password)
    x = u.load_user_by_username(cursor_, args.username)
    x = str(x)
    if args.username not in x:
        raise UniqueViolation("User not found")
    if u._hashed_password == u.hashed_password:
        u.delete(cursor_)
        print("User deleted")


def list_users():
    u = User()
    x = u.load_all_users(cursor_)
    x = str(x)
    print(x)


def main():
    u = User(args.username, args.password)
    if args.list is None and args.new_pass is None and args.delete is None and args.edit is None:
        check_user()
    if args.list is None and args.delete is None:
        edit_password()
    if args.list is None and args.edit is None and args.new_pass is None:
        delete_user()
    if args.list is not None:
        list_users()


if __name__ == '__main__':
    main()
