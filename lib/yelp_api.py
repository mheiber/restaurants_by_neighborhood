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
    """Prepares OAuth authentication and sends the request to the API.

    Args:
        host (str): The domain host of the API.
        path (str): The path of the API after the domain.
        url_params (dict): An optional set of query parameters in the request.

    Returns:
        dict: The JSON response from the request.

    Raises:
        urllib2.HTTPError: An error occurs from the HTTP request.
    """

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
    """Query the Search API by a search term and location.

    Args:
        term (str): The search term passed to the API.
        location (str): The search location passed to the API.

    Returns:
        dict: The JSON response from the request.
    """
    url_params = {
        'term': term.replace(' ', '+'),
        'location': location.replace(' ', '+'),
        # 'limit': SEARCH_LIMIT
    }
    return request(URL, credentials, params=url_params)


if __name__ == '__main__':
    # main()
   print  Ssearch('restaurant', 'georgetown, dc', credentials)
