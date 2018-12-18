import gapi_init
from bs4 import BeautifulSoup
from pprint import pprint
import base64
import time
import dateutil.parser as parser
from datetime import datetime
import datetime
import re

body_stop_regex = r'(.|\n|\r)*?(?=(\b((On Mon|On Tue|On Wed|On Thu|On Fri|On Sat|On Sun))\b)|(\b((În lun|În mar|În mie|În joi|În vin|În sâm|În dum))\b)|(--))'

class Mail:
    def __init__(self, author, date, content):
        self.author = author
        self.date = date
        self.content = content


def get_threads(gmail):
    thread_ids = gmail.users().threads().list(userId="me", labelIds=["Label_1"], maxResults=2).execute()
    threads = []

    for thread_id in thread_ids['threads']:
        t_id = thread_id['id']
        t = gmail.users().threads().get(userId = "me", id = t_id).execute()
        threads.append(t)

    return threads


def get_message_body(message):
    part_data = ""
    try:
        mssg_parts = message['payload']['parts']  # fetching the message parts
        part_one = mssg_parts[0]  # fetching first element of the part
        part_body = part_one['body']  # fetching body of the message
        part_data = part_body['data']  # fetching data from the body
        clean_one = part_data.replace("-", "+")  # decoding from Base64 to UTF-8
        clean_one = clean_one.replace("_", "/")  # decoding from Base64 to UTF-8
        clean_two = base64.b64decode(bytes(clean_one, 'UTF-8'))  # decoding from Base64 to UTF-8
        soup = BeautifulSoup(clean_two, "lxml")
        # print(soup.p.contents)
        body = re.match(body_stop_regex, soup.p.contents[0])
        return body.group(0).rstrip()
    except:
        print(part_data)
        return ""


def get_message_sender(message):
    payload = message['payload']
    header = payload['headers']

    for field in header:  # getting the Sender
        if field['name'] == 'From':
            msg_from = field['value']
            return msg_from
        else:
            pass
    return ""


def get_message_date(message):
    payload = message['payload']
    header = payload['headers']

    for field in header:  # getting the date
        if field['name'] == 'Date':
            msg_date = field['value']
            date_parse = (parser.parse(msg_date))
            return date_parse
        else:
            pass
    return ""


def parse_message(message):
    body = get_message_body(message)
    sender = get_message_sender(message)
    date = get_message_date(message)

    return Mail(sender, date, body)


def get_messages_from_threads(gmail, threads):
    messages = {}

    for thread in threads:
        for message in thread['messages']:
            mail_object = parse_message(message)
            print(vars(mail_object))


def get_aiurea_emails(gmail):

    threads = get_threads(gmail)
    messages = get_messages_from_threads(gmail, threads)


def main():
    gmail = gapi_init.auth()

    data = get_aiurea_emails(gmail)


if __name__ == "__main__":
    main()
