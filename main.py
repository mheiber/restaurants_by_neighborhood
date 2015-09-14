from lib import yelp_api
from lib.business import business_data
from lib.utils import dicts_to_csv, json_to_dict, validate_credentials
from lib.utils import safe_remove

# ! Fill CREDENTIALS_FILE out with correct Yelp API information
# You'll need a Yelp account
CREDENTIALS_FILE = 'credentials.json'
OUTPUT_FILE = 'restaurants_by_neighborhood.csv'

NEIGHBORHOODS = ['Columbia Heights, DC', 'Adams Morgan, DC']


def neighborhood_info(neighborhood):
    response = yelp_api.search('restaurant', neighborhood, credentials)
    raw_businesses = response['businesses']

    businesses = map(business_data, raw_businesses)
    return businesses


if __name__ == '__main__':
    credentials = json_to_dict(CREDENTIALS_FILE)
    validate_credentials(credentials)

    # start over
    safe_remove(OUTPUT_FILE)

    # neighborhoods_data is a list of business dictionaries
    # Each business dictionary will be a row in the output CSV
    neighborhoods_data = map(neighborhood_info, NEIGHBORHOODS)
    for neighborhood in neighborhoods_data:
        dicts_to_csv(neighborhood, OUTPUT_FILE, append=True)
