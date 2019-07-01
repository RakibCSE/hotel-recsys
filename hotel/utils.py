import requests

from datetime import datetime
from math import asin, cos, sqrt


def calculate_distance(lat1, lon1, lat2, lon2):
    p = 0.017453292519943295  # Pi/180
    a = 0.5 - cos((lat2 - lat1) * p) / 2 + cos(lat1 * p) * cos(lat2 * p) * (1 - cos((lon2 - lon1) * p)) / 2
    return 12742 * asin(sqrt(a))


def get_month(date_str):
    datetime_obj = datetime.strptime(date_str, "%d-%m-%Y")
    month = datetime_obj.strftime("%m")
    return int(month)


def get_year(date_str):
    datetime_obj = datetime.strptime(date_str, "%d-%m-%Y")
    year = datetime_obj.strftime("%Y")
    return int(year)


def get_user_ip():
    response = requests.get("http://ip-api.com/json")
    user_ip = response.json()['query']
    return user_ip
