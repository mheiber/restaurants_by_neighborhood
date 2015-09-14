"""
Search Yelp API

portions of this code adapted from
http://www.yelp.com/developers/documentation
"""
import urllib2
import oauth2
import json
from utils import stringed_dict

URL = 'http://api.yelp.com/v2/search/'


def request(url, credentials, params={}):

    # for some crazy reason, oauth lib requires strings instead of unicode
    c = stringed_dict(credentials)

    consumer = oauth2.Consumer(c['consumer_key'], c['consumer_secret'])
    oauth_request = oauth2.Request(method="GET", url=url, parameters=params)

    oauth_request.update(
        {
            'oauth_nonce': oauth2.generate_nonce(),
            'oauth_timestamp': oauth2.generate_timestamp(),
            'oauth_token': c['token'],
            'oauth_consumer_key': c['consumer_key']
        }
    )
    token = oauth2.Token(c['token'], c['token_secret'])
    sha1 = oauth2.SignatureMethod_HMAC_SHA1()
    oauth_request.sign_request(sha1, consumer, token)
    signed_url = oauth_request.to_url()

    print u'Querying {0} ...'.format(url)

    conn = urllib2.urlopen(signed_url, None)
    try:
        response = json.loads(conn.read())
    finally:
        conn.close()

    return response


def search(term, location, credentials):
    url_params = {
        'term': term.replace(' ', '+'),
        'location': location.replace(' ', '+'),
        # 'limit': SEARCH_LIMIT
    }
    return request(URL, credentials, params=url_params)
