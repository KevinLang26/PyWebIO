from pywebio.output import *
from pywebio.session import *
from pywebio.pin import *
import json
import time
import requests
import os
from functools import partial

from main import put_sub_feed


def main():
    file_exist = os.path.exists('subscriptions.json')

    if not file_exist:
        put_text("You are not following anyone")
    else:
        put_code("Stories submitted by users that I follow")
        put_text("Feed")
        with open('subscriptions.json', 'r+') as files:
            a_dict = json.load(files)
            put_sub_feed(a_dict["subscribed"])

start_server(main, port=8080, debug=True)


#Build jazzy version

from pywebio.output import *
import json
import os
from Functions import put_sub_feed

lists = ['']
a_dict = {''}
list = set()


def main():
    file_exist = os.path.exists('subscriptions.json')

    if not file_exist:
        put_text("You are not following anyone")
    else:
        put_code("Stories submitted by users that I follow")
        put_text("Feed")
        with open('subscriptions.json', 'r+') as files:
            a_dict = json.load(files)
            put_sub_feed(a_dict["subscribed"])

