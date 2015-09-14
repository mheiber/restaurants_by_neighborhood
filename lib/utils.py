from datetime import datetime
import json
import os
import csv


def cur_year_month_day():
    now = datetime.now().timetuple()
    return (now.tm_year, now.tm_mon, now.tm_mday)


def stringed_dict(dictionary):
    new_dict = {}
    for key in dictionary.keys():
        new_dict[str(key)] = str(dictionary[key])

    return new_dict


def json_to_dict(json_file_name):
    with open(json_file_name, 'r') as f:
        return json.loads(f.read())


def dicts_to_csv(dicts, csv_file_name, append=False):
    if not os.path.isfile(csv_file_name):
        append = False
    mode = 'ab' if append else 'wb'
    with open(csv_file_name, mode) as f:
        writer = csv.writer(f)
        headers = dicts[0].keys()
        if not append:
            writer.writerow(headers)
        rows = [row.values() for row in dicts]

        writer.writerows(rows)


def validate_credentials(credentials_dict):
    if credentials_dict['consumer_key'] == 'my consumer key':
        raise Exception('Please edit {} with real Yelp API credentials'.format(
            credentials_dict))


def safe_remove(file_name):
    try:
        os.remove(file_name)
    except OSError:
        pass
