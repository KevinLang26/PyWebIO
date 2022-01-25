from pywebio import start_server
from pywebio.input import *
from pywebio.output import *
from pywebio.session import *
from pywebio.pin import *
import json
import time
import requests
def main():

    username = input('Enter user you are looking for', type=TEXT)
    api = (requests.get('https://hacker-news.firebaseio.com/v0/user/'+username+'.json?print=pretty'))
    data = api.text
    info = json.loads(data)
    submitted = info['submitted']
    for i in submitted:
        api2 =(requests.get('https://hacker-news.firebaseio.com/v0/item/'+str(i)+'.json?print=pretty'))
        data2 = api2.text
        info2 = json.loads(data2)
        time1 = info2['time']
        if int(time.time()) - time1 <= 86400:
            try:
                put_processbar('bar');
                for i in range(1, 11):
                    set_processbar('bar', i / 10)
                    time.sleep(0.05)
                put_code(info2['title'])
                put_code(info2['url'])
            except KeyError:
                continue
start_server(main, port=8080, debug=True)

