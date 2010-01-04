import irc
import twitter
import message_queue

import time

username = "wdw_irc"
password = raw_input("the password, please: ")

def process_message(data):
    if data['username'] == 'wdw':
        twitter.post_tweet(username, password, data['message'])

irc = irc.IRC("IoTbot", "IRC over Twitter python bot")
commands = {}
channels = {}
queue = message_queue.MessageQueue(irc, 2)

irc.register_callback('channel_message', process_message)
irc.connect('irc.freenode.net', 6667)

irc.join('#slicehost')

last_time = time.time()

while True:
    irc.read()
    if time.time() - last_time > 20:
        last_time = time.time()
        twitter.check_twitter('udev_random', password, queue)
        queue.process_message_queue()
    time.sleep(2)
