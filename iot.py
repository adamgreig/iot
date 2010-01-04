import irc
import twitter
import message_queue

import socket
import time
import sys
import urllib2
from xml.dom import minidom

username = "wdw_irc"
password = "#############"

last_status = ""

twitter_feed_url = "http://twitter.com/statuses/user_timeline/%s.rss"

def process_message(data):
    if data['username'] == 'wdw':
        twitter.post_tweet(username, password, data['message'])

def check_twitter(username, queue):
    global last_status
    feed_url = twitter_feed_url % username
    f = urllib2.urlopen(feed_url)
    xmldoc = minidom.parse(f)
    items = xmldoc.getElementsByTagName('item')
    if items:
        item = items[0]
        status = item.getElementsByTagName('description')[0].firstChild
        if status:
            status = status.data
            if status != last_status:
                queue.addSayMessage('<wdw> ' + status, '#slicehost')
                last_status = status

irc = irc.IRC("IoTbot", "IRC over Twitter python bot")
commands = {}
channels = {}
queue = message_queue.MessageQueue(irc, 2)

irc.register_callback('channel_message', process_message)
irc.connect('irc.freenode.net', 6667)

irc.join('#slicehost')

while True:
    irc.read()
    check_twitter('udev_random', queue)
    queue.process_message_queue()
    time.sleep(5)
