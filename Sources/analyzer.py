import pickle
from collections import Counter
from importer import Mail
import plots
import numpy as np
import pandas as pd
from nltk.tokenize import TweetTokenizer


class Aiureapedia:

    def __init__(self):
        self.members = {}
        self.vocabulary = Counter()
        self.tokenizer = TweetTokenizer(preserve_case=False)

    def add_message_to_member(self, address, name, date, content):
        tokenized = self.tokenizer.tokenize(content)
        message = Message(content, tokenized, date)

        if address not in self.members:
            member = Member(address, name)
            member.add_message(message)
            self.members[address] = member
        else:
            member = self.members[address]
            member.add_message(message, )

    def finalize(self):
        for member in self.members.values():
            member.finalize()
            self.vocabulary = self.vocabulary + member.vocabulary

    def get_dates(self):
        return [message.date for member in self.members.values() for message in member.messages]


class Member:

    def __init__(self, address, name):
        self.id = address
        self.alias = name

        self.messages = []
        self.vocabulary = Counter()

    def finalize(self):
        for message in self.messages:
            for token in message.tokens:
                self.vocabulary[token] += 1

    def add_message(self, message):
        self.messages.append(message)

    def message_count(self):
        return len(self.messages)

    def word_count(self):
        return sum([len(m.tokens) for m in self.messages])

    def get_dates(self):
        return [message.date for message in self.messages]


class Message:

    def __init__(self, content, tokenized, date):
        self.content = content
        self.tokens = tokenized
        self.date = date



def get_author(message):
    name, address = message.author.split("<")
    return name, address.replace(">","")


def delete_last_line(text):
    lines = text.splitlines()
    if len(lines) > 2 and lines[-2] == "":
        return "\n".join(lines[:-2])
    else:
        return text



def build_dictionary(data):
    d = Aiureapedia()

    for message in data:
        name, address = get_author(message)
        if(address == r'ionel.covasan@gmail.com'):
            content = delete_last_line(message.content)
        else:
            content = message.content
        d.add_message_to_member(address, name, message.date, content)

    d.finalize()

    return d


def get_top_posters(d, n = 25):
    count_stat = dict([(member.alias, member.message_count()) for member in d.members.values()])
    count_stat = sorted(count_stat.items(), key=lambda kv: kv[1], reverse=True)
    top_posters = [member[0] for member in count_stat[:n]]
    return top_posters

def mail_count(d):
    count_stat = dict([(member.alias, member.message_count()) for member in d.members.values()])
    count_stat = sorted(count_stat.items(), key=lambda kv: kv[1], reverse = True)
    plots.plot_bar_chart(count_stat, "")
    print(count_stat)


def number_of_words(d):
    words_stat = dict([(member.alias, member.word_count()) for member in d.members.values()])
    words_stat = sorted(words_stat.items(), key=lambda kv: kv[1], reverse= True)
    plots.plot_bar_chart(words_stat, "")


def avg_words_per_mail(d):
    top_posters = get_top_posters(d)
    avg_stat = dict([(member.alias, member.word_count() / member.message_count()) for member in d.members.values() if member.alias in top_posters])
    avg_stat = sorted(avg_stat.items(), key=lambda kv: kv[1], reverse= True)
    plots.plot_bar_chart(avg_stat, "")


def day_of_week(d):
    dates = d.get_dates()
    message_day = np.zeros(7)
    for d in dates:
        message_day[d.weekday()] += 1
    plots.plot_day_bar_chart(message_day)


def time_of_day(d):
    dates = d.get_dates()
    hours = [d.hour + (d.minute / 60) for d in dates]
    plots.plot_clock_histogram(hours)


def hours_per_member(d):
    top_posters = get_top_posters(d, 10)
    time_stat = dict([(member.alias, [d.hour + (d.minute / 60) for d in member.get_dates()]) for member in d.members.values() if member.alias in top_posters])
    plots.plot_time_density(time_stat)

def get_stats(d):

    #mail_count(d)
    #number_of_words(d)
    #avg_words_per_mail(d)
    #day_of_week(d)
    #time_of_day(d)
    hours_per_member(d)


def main():
    data = pickle.load(open("../DataDumps/mailDump.p", "rb"))
    d = build_dictionary(data)

    get_stats(d)
    print(len(data))



if __name__=='__main__':
    main()