import warnings
import json
import logging
import pickle
import pandas as pd
import requests

from datetime import datetime
from math import asin, cos, sqrt

from geoip2 import webservice
from sklearn.tree import DecisionTreeClassifier

from .models import UserInteraction, UserSearch


logger = logging.getLogger("utils")


def save_search_data(request, query_data, booking=0):
    """
    Save user interaction data.

    Args:
        request:
        query_data: Queryset data
        booking: Hotel is booked or not
    """

    account_id = 141975
    license_key = "Uf4x3NwFVldx"
    room = adult = children = 0

    country_data = get_country_data()
    client = webservice.Client(account_id, license_key)
    user_ip = get_user_ip()
    response = client.insights(ip_address=user_ip)

    session_data = request.session
    checkin_date = session_data['check_in_date']
    checkout_date = session_data['check_out_date']
    if session_data['room']:
        room = int(session_data['room'])
    if session_data['adult']:
        adult = int(session_data['adult'])
    if session_data['children']:
        children = int(session_data['children'])

    date_today = datetime.today().strftime("%d-%m-%Y")

    hotel_latitude = query_data.hotel_latitude
    hotel_longitude = query_data.hotel_longitude
    user_latitude = response.location.latitude
    user_longitude = response.location.longitude
    orig_distance = calculate_distance(user_latitude, user_longitude,
                                       hotel_latitude, hotel_longitude)

    user_interaction_obj = UserInteraction()

    if request.user.id:
        user_interaction_obj.user_id = request.user.id
    else:
        user_interaction_obj.user_id = 0

    search_data = UserSearch.objects.filter(
        hotel_id=query_data.hotel_id, keyword=session_data['place']).count()
    if search_data:
        search_data = UserSearch.objects.get(
            hotel_id=query_data.hotel_id, keyword=session_data['place'])
        search_data.counter += 1
        search_data.save()
    else:
        user_search_obj = UserSearch()
        user_search_obj.keyword = session_data['place']
        user_search_obj.hotel_id = query_data.hotel_id
        user_search_obj.hotel_cluster = query_data.cluster
        user_search_obj.counter += 1
        user_search_obj.save()

    user_interaction_obj.hotel_id = query_data.hotel_id
    user_interaction_obj.date_time_year = get_year(date_today)
    user_interaction_obj.date_time_month = get_month(date_today)
    user_interaction_obj.srch_ci_year = get_year(checkin_date)
    user_interaction_obj.srch_ci_month = get_month(checkin_date)
    user_interaction_obj.srch_co_year = get_year(checkout_date)
    user_interaction_obj.srch_co_month = get_month(checkout_date)
    user_interaction_obj.hotel_country = country_data[query_data.country.lower(
    )]
    user_interaction_obj.user_location_country = country_data[response.country.name.lower(
    )]
    user_interaction_obj.user_location_city = response.city.geoname_id
    user_interaction_obj.user_location_region = response.subdivisions.most_specific.geoname_id
    user_interaction_obj.is_booking = booking
    user_interaction_obj.orig_destination_distance = orig_distance
    user_interaction_obj.srch_destination_id = query_data.district_id
    user_interaction_obj.srch_rm_cnt = room
    user_interaction_obj.srch_adults_cnt = adult
    user_interaction_obj.srch_children_cnt = children
    user_interaction_obj.hotel_cluster = query_data.cluster
    user_interaction_obj.save()


def get_recommendations(request, data_list):
    """
    Returns recommended hotel clusters and hotel country code

    Args:
        request: Request
        data_list: Search result list

    Returns:
        recommended_cluster: Clusters recommended for hotels.
    """
    try:
        countries = []
        hotel_countries = []
        recommended_cluster = []
        user_interactions = []

        try:
            with open("hotel/recsys-ml.pickle", "rb") as pickle_file:
                loaded_model = pickle.load(pickle_file)
        except FileNotFoundError as err:
            print(err)

        try:
            countries = list(set([data["country_id"]
                                  for data in list(data_list.values())]))
            user_interactions = list(UserInteraction.objects.filter(
                hotel_country__in=countries).values())
        except Exception as err:
            print(err)

        if user_interactions:
            data_df = pd.DataFrame(user_interactions)
            data_x = data_df.drop(["id", "user_id", "hotel_id", "is_booking"], axis=1)

            recommended_cluster = list(set(loaded_model.predict(data_x)))

        return recommended_cluster

    except Exception as err:
        print(err)


def calculate_distance(lat1, lon1, lat2, lon2):
    """
    Returns distance between two location points.

    Args:
        lat1: User latitude
        lon1: User longitude
        lat2: Hotel latitude
        lon2: Hotel longitude

    Returns:
        total_distance: The distance between two location points.
    """
    p = 0.017453292519943295  # Pi/180
    a = 0.5 - cos((lat2 - lat1) * p) / 2 + cos(lat1 * p) * \
        cos(lat2 * p) * (1 - cos((lon2 - lon1) * p)) / 2
    total_distance = 12742 * asin(sqrt(a))
    return total_distance


def get_month(date_str):
    """
    Returns month from the date string

    Args:
        date_str: Date string

    Returns:
        month: Month in interger 
    """
    datetime_obj = datetime.strptime(date_str, "%d-%m-%Y")
    month = datetime_obj.strftime("%m")
    return int(month)


def get_year(date_str):
    """
    Returns year from the date string

    Args:
        date_str: Date string

    Returns:
        year: Year in interger 
    """
    datetime_obj = datetime.strptime(date_str, "%d-%m-%Y")
    year = datetime_obj.strftime("%Y")
    return int(year)


def get_user_ip():
    """
    Get the user ip address.

    Returns:
        user_ip: IP address of the user.
    """
    response = requests.get("http://ip-api.com/json/")
    user_ip = response.json()['query']
    return user_ip


def get_user_city_country():
    """
    Get the user city and country.

    Returns:
        user_city:
        user_country:
    """
    response = requests.get("http://ip-api.com/json/")
    print(response.json())
    user_country = response.json()["country"]
    user_city = response.json()["city"]
    return user_city, user_country


def get_country_data():
    """
    Returns country data with country codes

    Returns:
        json_data: Country json data
    """
    json_data = {}
    with open("hotel/country.json", "rb") as json_fp:
        json_data = json.load(json_fp)
    return json_data


def train_algorithm():
    """
    Train the user interactions data by algorithm.
    """

    interaction_data = list(UserInteraction.objects.all().values())

    # Convert to DataFrame
    int_data_df = pd.DataFrame(interaction_data)

    # Dividing train data for X and Y
    train_x = int_data_df.drop(
        ["id", "user_id", "hotel_id", "is_booking"], axis=1)
    train_y = int_data_df.hotel_cluster

    # Algorithm initiation and fit the model
    algorithm_clf = DecisionTreeClassifier(max_depth=10, random_state=0)
    algorithm_clf.fit(train_x, train_y)

    pickle.dump(algorithm_clf, open("hotel/recsys-ml.pickle", 'wb'))


def warn(*args, **kwargs):
    pass


warnings.warn = warn
