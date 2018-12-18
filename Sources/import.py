import gapi_init
from bs4 import BeautifulSoup
from pprint import pprint
import base64
import re

body_stop_regex = r'(.|\n|\r)+?(?=\b((On Mon|On Tue|On Wed|On Thu|On Fri|On Sat|On Sun))\b)'

def get_aiurea_emails(gmail):

    threads = gmail.users().threads().list(userId = "me", labelIds = ["Label_1"])


    mailid = gmail.users().messages().list(userId = "me", labelIds = ["Label_1"], maxResults = 2).execute()
    message = gmail.users().messages().get(userId = "me", id = mailid['messages'][1]['id']).execute()

    mssg_parts = message['payload']['parts']  # fetching the message parts
    part_one = mssg_parts[0]  # fetching first element of the part
    part_body = part_one['body']  # fetching body of the message
    part_data = part_body['data']  # fetching data from the body
    clean_one = part_data.replace("-", "+")  # decoding from Base64 to UTF-8
    clean_one = clean_one.replace("_", "/")  # decoding from Base64 to UTF-8
    clean_two = base64.b64decode(bytes(clean_one, 'UTF-8'))  # decoding from Base64 to UTF-8
    soup = BeautifulSoup(clean_two, "lxml")
    body = re.match(body_stop_regex, soup.p.contents[0])
    print(body.group(0).rstrip())

def main():
    gmail = gapi_init.auth()

    data = get_aiurea_emails(gmail)


if __name__ == "__main__":
    main()
