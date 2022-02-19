from pywebio import start_server
from pywebio.input import *
from pywebio.output import *
from pywebio.session import *
from pywebio.pin import *


from main import put_feed



def main():
    put_input('usernames', label='Enter the user(s) you are looking for',
              placeholder='Multiple users can be entered seperated by ";"')
    put_buttons(['Search'], lambda _: put_feed(pin.usernames))


start_server(main, port=8080, debug=True)



# Build jazzy app version 
from pywebio.input import *
from pywebio.output import *
from pywebio.session import *
from pywebio.pin import *


from Functions import put_feed
from Functions import subscribe



def main():
    put_input('usernames', label='Enter the user(s) you are looking for',
              placeholder='Multiple users can be entered seperated by ";"')
    put_buttons(['Search'], lambda _: put_feed(pin.usernames))

