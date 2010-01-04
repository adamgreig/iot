import urllib2
import urllib
import logging
from xml.dom import minidom

last_status = ""
twitter_feed_url = "http://twitter.com/statuses/user_timeline/%s.rss"

def check_twitter(username, queue):
    global last_status
    global twitter_feed_url
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

def post_tweet(username, password, tweet):
    twitter = "http://twitter.com/statuses/update.xml"
    req_payload = {'status':tweet}
    auth_man = urllib2.HTTPPasswordMgrWithDefaultRealm()
    auth_man.add_password(None, twitter, username, password)
    auth_handler = urllib2.HTTPBasicAuthHandler(auth_man)
    urllib2.install_opener(urllib2.build_opener(auth_handler))
    data = urllib.urlencode(req_payload)

    try:
        resp = urllib2.urlopen(urllib2.Request(twitter, data))
        status = resp.read
    except urllib2.URLError, e:
        if hasattr(e, 'reason'):
            logging.critical("Unable to reach twitter - %s", e.reason)
        elif hasattr(e, 'code'):
            logging.critical("Error on Twitter - %s", e.code)
            raise

