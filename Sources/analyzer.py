import pickle
from collections import Counter
from importer import Mail


class Aiureapedia:

    def __init__(self):
        self.members = {}

    def add_message_to_member(self, address, name, date, content):
        message = Message(content, date)

        if address not in self.members:
            member = Member(address, name)
            member.add_message(message)
            self.members[address] = member
        else:
            member = self.members[address]
            member.add_message(message)


class Member:

    def __init__(self, address, name):
        self.id = address
        self.alias = Counter()
        self.alias[name] += 1

        self.messages = []

    def add_message(self, message):
        self.messages.append(message)

    def get_name(self):
        return self.alias.most_common(1)[0][0]

    def message_count(self):
        return len(self.messages)


class Message:

    def __init__(self, content, date):
        self.date = date
        self.content = content



def get_author(message):
    name, address = message.author.split("<")
    return name, address.replace(">","")


def build_dionary(data):
    d = Aiureapedia()

    for message in data:
        name, address = get_author(message)
        d.add_message_to_member(address, name, message.date, message.content)

    return d


def mail_count(d):
    count_stat = dict([(member.get_name(), member.message_count()) for member in d.members.values()])
    count_stat = sorted(count_stat.items(), key=lambda kv: kv[1])
    count_stat.reverse()

    print(count_stat)


def get_stats(d):

    mail_count(d)


def main():
    data = pickle.load(open("../DataDumps/mailDump.p", "rb"))
    d = build_dionary(data)

    get_stats(d)
    print(len(data))



if __name__=='__main__':
    main()