import urllib2
import urllib
import logging

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

