import argparse
from models import Messages, User
import psycopg2

conn = psycopg2.connect(database='demo_db', user='postgres', password='password', host='localhost', port='5432')
conn.autocommit = True
cursor_ = conn.cursor()

parser = argparse.ArgumentParser()
parser.add_argument("-u", "--username", help="username")
parser.add_argument("-p", "--password", help="password")
parser.add_argument("-l", "--list", help="list all messages", action="store_true")
parser.add_argument("-t", "--to", help="to")
parser.add_argument("-s", "--send", help="message to send")

args = parser.parse_args()


def print_user_messages():
    messages = Messages.load_all_messages(cursor_)
    for message in messages:
        from_ = User.load_user_by_id(cursor_, message.from_id)
        print(20 * "-")
        print(f"from: {from_.username}")
        print(f"data: {message.creation_date}")
        print(message.text)
        print(20 * "-")


def send_message(cur, from_id, recipient_name, text):
    if len(text) > 255:
        print("Message is too long!")
        return
    to = User.load_user_by_username(cur, recipient_name)
    if to:
        message = Messages(from_id, to.id, text=text)
        message.save_to_db(cur)
        print("Message send")
    else:
        print("Recipient does not exists.")


def main():
    if args.username and args.password and args.list:
        print_user_messages()
    if args.to:
        send_message(cursor_, 15, "Johnny", "ziom")


if __name__ == '__main__':
    main()
