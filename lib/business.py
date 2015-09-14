from lxml.cssselect import CSSSelector as Sel
from lxml.html import fromstring
from collections import OrderedDict

from utils import cur_year_month_day
import requests
import re


def _raw_price_from_string(html_str):
    html = fromstring(html_str)
    el = Sel('.price-description')(html)[0]
    return el.text.strip()


def raw_price(url):
    '''returns stuff like "Under $10" or "$10-20"'''
    response = requests.get(url)
    return _raw_price_from_string(response.content)


def clean_price_or_none(raw_price_string):

    def average(nums):
        return sum(nums) / float(len(nums))

    price = None

    try:
        # grab price if only one price is given
        # otherwise give average price
        prices_strings = re.findall(r'[0-9]+', raw_price_string)
        prices = map(float, prices_strings)

        price = average(prices)

    except Exception as e:
        print e
    return price


def business_data(raw_biz):
    biz = OrderedDict()

    biz['name'] = raw_biz['name']

    url = raw_biz['url']
    biz['url'] = url

    biz['address'] = raw_biz['location']['address'][0]
    biz['neighborhood'] = raw_biz['location']['neighborhoods'][0]
    biz['zip_code'] = raw_biz['location']['postal_code']
    biz['rating'] = raw_biz['rating']

    raw_price_string = raw_price(url)

    biz['raw_price'] = raw_price_string

    biz['price'] = clean_price_or_none(raw_price_string)

    y, m, d = cur_year_month_day()

    biz['retrieval_year'] = y
    biz['retrieval_month'] = m
    biz['retrival_day'] = d

    return biz


if __name__ == '__main__':
    html_str = '<html><div class="price-description">\nUnder $10</div></html>'
    price = _raw_price_from_string(html_str)
    assert(price == 'Under $10')

    # SLOW test
    url = 'http://www.yelp.com/biz/simply-banh-mi-washington-2'
    price2 = raw_price(url)
    assert(len(price2) > 2)
    assert('$' in price2)

    assert(clean_price_or_none('Under $10') == 10.0)
    assert(clean_price_or_none('$10-20') == 15.0)
