from pywebio import start_server
from pywebio.input import *
from pywebio.output import *
from pywebio.session import *
from pywebio.pin import *
import json
import time
import requests
import os


def split(username):
    username = username.replace(" ", "")
    users = username.split(";")
    for i in users:
        put_row([put_text(str(i)), put_buttons(['Subscribe'], lambda _: subscribe(i))])
        retrieve_subtime(retrieve_usersubmissions(str(i)))


def retrieve_usersubmissions(user):
    api = (requests.get('https://hacker-news.firebaseio.com/v0/user/' + user + '.json?print=pretty'))
    data = api.text
    info = json.loads(data)
    submitted = info["submitted"]
    return submitted


def retrieve_subtime(submission):
    for x in submission:
        api2 = (requests.get('https://hacker-news.firebaseio.com/v0/item/' + str(x) + '.json?print=pretty'))
        data2 = api2.text
        info2 = json.loads(data2)
        time1 = info2["time"]
        if int(time.time()) - time1 <= 86400:
            if "type" in info2.keys() and info2["type"] == 'story' and "dead" not in info2.keys() and check_dup(
                    info2["url"]):
                put_link(info2["title"], info2["url"], new_window=True)
                put_text()
            else:
                continue
        else:
            break


def check_dup(url):
    if url in lists:
        return False
    else:
        lists.append(url)
        return True


def subscribe(user):
    file_exist = os.path.exists('subscriptions.json')
    if not file_exist:
        a_dict = {}
        a_dict["subscribed"] = [user]
        with open("subscriptions.json", 'w+') as file:
            json.dump(a_dict, file)
        put_text("subscribed to %s" % user)
    else:
        with open('subscriptions.json', 'r+') as files:
            a_dict = json.load(files)
            if user in a_dict["subscribed"]:
                put_text("Already subscribed to %s" % user)
                return
            else:
                a_dict["subscribed"].append(user)
        with open("subscriptions.json", 'w+') as file:
            json.dump(a_dict, file)
        put_text("subscribed to %s" % user)


def unfollow(user):
    file_exist = os.path.exists('subscriptions.json')
    if not file_exist:
        put_text("You are not subscribed to anyone")
    else:
        a_dict = {}
        with open('subscriptions.json', 'r+') as files:
            a_dict = json.load(files)
            if user not in a_dict["subscribed"]:
                put_text("You are not subscribed to %s" % user)
                return
            else:
                a_dict["subscribed"].remove(user)
        with open("subscriptions.json", 'w+') as file:
            json.dump(a_dict, file)

    put_text("unfollowed %s" % user)


def feed(users):
    for i in users:
        put_text(str(i))
        retrieve_subtime(retrieve_usersubmissions(str(i)))


lists = ['']
a_dict = {''}


def main():

    file_exist = os.path.exists('subscriptions.json')
    put_input('usernames', label='Enter the user(s) you are looking for',placeholder='Multiple users can be entered seperated by ";"')
    put_buttons(['Search'], lambda _: split(pin.usernames))
    put_row([put_code('Subscribed Feed')])

    #put_input('User', label='Subscription', placeholder='User')
    #[put_buttons(['Subscribe'], lambda _: subscribe(pin.User))
    #put_buttons(['Unfollow'], lambda _: unfollow(pin.User))


    if not file_exist:
        put_text("You are not following anyone")
    else:
        with open('subscriptions.json', 'r+') as files:
            a_dict = json.load(files)
            feed(a_dict["subscribed"])
    [put_code('Feed')]
    lists.clear()



start_server(main, port=8080, debug=True)
