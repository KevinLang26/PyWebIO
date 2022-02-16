from pywebio import start_server
from pywebio.input import *
from pywebio.output import *
from pywebio.session import *
from pywebio.pin import *
import json
import time
import requests
import os
from functools import partial


def output(username):
            #This function takes the input from the user of the app and turns it into instructions the code can user
    username = username.replace(" ", "")    #Removes any spacebars between users accidentally input
    users = username.split(";")     #splits the string input into a list of user profiles
    for i in users:   #instructs code to output information one user at a time
        put_row([put_text(str(i)), put_buttons(['Subscribe'], onclick = partial(subscribe, id=i))])
        retrieve_storylink(retrieve_usersubmissions(str(i)))



def retrieve_usersubmissions(user):
            #grabs the user submission data from hackernews api
    api = (requests.get('https://hacker-news.firebaseio.com/v0/user/' + user + '.json?print=pretty'))
    data = api.text
    info = json.loads(data)
    submitted = info["submitted"]
    return submitted


def retrieve_storylink(submission):
            #using information from retreive_usersubmissions finds valid recent story links and output them
    for x in submission:
        api2 = (requests.get('https://hacker-news.firebaseio.com/v0/item/' + str(x) + '.json?print=pretty'))
        data2 = api2.text
        info2 = json.loads(data2)
        time1 = info2["time"]
        if int(time.time()) - time1 <= 86400:
            if "type" in info2.keys() and info2["type"] == 'story' and "title" in info2.keys() and "url" in info2.keys() and "dead" not in info2.keys() and check_dup(info2["url"]):
                put_link(info2["title"], info2["url"], new_window=True)
                put_text()
            else:
                continue
        else:
            break


def check_dup(url):
            #mkaes sure duplicate stories arent output
    if url in lists:
        return False
    else:
        lists.append(url)
        return True


def subscribe(user, id):
            #cretes subscriptions list and adds users for subscription feed
    file_exist = os.path.exists('subscriptions.json')
    if not file_exist:
        a_dict = {}
        a_dict["subscribed"] = [id]
        with open("subscriptions.json", 'w+') as file:
            json.dump(a_dict, file)
        put_text("subscribed to %s" % id)
    else:
       with open('subscriptions.json', 'r+') as files:
            a_dict = json.load(files)
            if id in a_dict["subscribed"]:
                put_text("Already subscribed to %s" % id)
                return
            else:
                a_dict["subscribed"].append(id)
       with open("subscriptions.json", 'w+') as file:
           json.dump(a_dict, file)
       put_text("subscribed to %s" % id)





def unfollow(user, id):
            #same to subscribe function but the opposite// removes users
    file_exist = os.path.exists('subscriptions.json')
    if not file_exist:
        put_text("You are not subscribed to anyone")
    else:
        a_dict = {}
        with open('subscriptions.json', 'r+') as files:
            a_dict = json.load(files)
            if id not in a_dict["subscribed"]:
                put_text("You are not subscribed to %s" % id)
                return
            else:
                a_dict["subscribed"].remove(id)
        with open("subscriptions.json", 'w+') as file:
            json.dump(a_dict, file)

    put_text("unfollowed %s" % id)


def feed(users):
            #output Subscription feed links
    for i in users:
        put_row([put_text(str(i)), put_buttons(['Unfollow'], onclick = partial(unfollow, id=i))])
        retrieve_storylink(retrieve_usersubmissions(str(i)))


lists = ['']
a_dict = {''}
list = set()

def main():

    file_exist = os.path.exists('subscriptions.json')

    put_input('usernames', label='Enter the user(s) you are looking for',placeholder='Multiple users can be entered seperated by ";"')
    put_buttons(['Search'], lambda _: output(pin.usernames))
    put_row([put_code('Subscribed Feed')])


    if not file_exist:
        put_text("You are not following anyone")
    else:
        with open('subscriptions.json', 'r+') as files:
            a_dict = json.load(files)
            feed(a_dict["subscribed"])
    [put_code('Feed')]
    lists.clear()



start_server(main, port=8080, debug=True)
