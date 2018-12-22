import gapi_init
from bs4 import BeautifulSoup
from pprint import pprint
import base64
import time
import dateutil.parser as parser
import re
import pickle


body_stop_regex = r'^((\b((On Mon|On Tue|On Wed|On Thu|On Fri|On Sat|On Sun))\b)|(\b((În lun|În mar|În mie|În joi|În vin|În sâm|În dum))\b)|(--)|(\b(Vlad Helgiu)\b)|(\*______________________\*)|(Best regards,)|(\*+))'

failed = []

class Mail:
    def __init__(self, author, date, content):
        self.author = author
        self.date = date
        self.content = content


def get_threads(gmail):
    thread_ids = gmail.users().threads().list(userId="me", labelIds=["Label_1"], maxResults=300).execute()
    threads = []

    len_t = len(thread_ids['threads'])
    i=0
    for thread_id in thread_ids['threads']:
        print(f"{i}/{len_t}")
        t_id = thread_id['id']
        t = gmail.users().threads().get(userId = "me", id = t_id).execute()
        threads.append(t)
        i += 1

    return threads


def get_message_body(message):
    try:
        mssg_parts = message['payload']['parts']  # fetching the message parts
        part_one = mssg_parts[0]  # fetching first element of the part
        while part_one['mimeType'] == r'multipart/alternative':
            part_one = part_one['parts'][0]
        part_body = part_one['body']  # fetching body of the message
        part_data = part_body['data']  # fetching data from the body
        clean_one = part_data.replace("-", "+")  # decoding from Base64 to UTF-8
        clean_one = clean_one.replace("_", "/")  # decoding from Base64 to UTF-8
        clean_two = base64.b64decode(bytes(clean_one, 'UTF-8'))  # decoding from Base64 to UTF-8
        soup = BeautifulSoup(clean_two, "lxml")
    except:
        failed.append(message)
        return ""

    body = ""
    if soup.p:
        for line in soup.p.contents[0].splitlines():
            if not re.match(body_stop_regex, line):
                body = "\n".join([body, line])
            else:
                break
    return body.replace(r"[image: image.png]", "").lstrip().rstrip()


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
    mails = []

    i = 0
    total = 0
    len_t = len(threads)
    for thread in threads:
        ii = 0
        for message in thread['messages']:
            total += 1
            len_m = len(thread['messages'])
            mail_object = parse_message(message)
            mails.append(mail_object)
            print(f"thread {i}/{len_t}, message {ii}/{len_m}")
            ii += 1
        i += 1

    print(total)
    return mails

def get_aiurea_emails(gmail):

    #threads = get_threads(gmail)
    #pickle.dump(threads, open("../DataDumps/threadsDump.p", "wb"))

    threads = pickle.load(open("../DataDumps/threadsDump.p", "rb"))
    #mail_object = parse_message(threads[18]['messages'][2])
    #print(vars(mail_object))
    mails = get_messages_from_threads(gmail, threads)

    return mails


def process():
    gmail = gapi_init.auth()

    data = get_aiurea_emails(gmail)

    pickle.dump(data, open("../DataDumps/mailDump.p", "wb"))
    pickle.dump(failed, open("../DataDumps/failDump.p", "wb"))


def inspect_bad(bad):
    mssg_parts = bad['payload']['parts']  # fetching the message parts
    part_one = mssg_parts[0]  # fetching first element of the part
    part_body = part_one['parts'][0]['body']  # fetching body of the message
    print(part_one['parts'][0])
    #part_data = part_body['data']  # fetching data from the body


def inspect():
    good = pickle.load(open("../DataDumps/mailDump.p", "rb"))
    bad = pickle.load(open("../DataDumps/failDump.p", "rb"))

    print(len(good))
    print(len(bad))

    inspect_bad(bad[1])


def main():
    #process()
    inspect()


if __name__ == "__main__":
    main()
