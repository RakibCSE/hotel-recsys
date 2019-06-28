import pandas as pd

from datetime import datetime

from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.postgres.search import SearchVector
from django.views.decorators.csrf import csrf_exempt

from geoip2 import webservice
from ipware import get_client_ip


from .models import HotelDetail, UserInteraction
from ml_engine.models import RecommendedData


def save_search_data(request):

    if request.GET:
        account_id = 141975
        license_key = "Uf4x3NwFVldx"
        user_ip = get_client_ip(request)

        client = webservice.Client(account_id, license_key)
        # response = client.insights(ip_address=user_ip)

        get_data = request.GET

        user_interaction_obj = UserInteraction()
        # user_interaction_obj.user_id = request.user.id
        user_interaction_obj.hotel_id = ""
        user_interaction_obj.checkin_date_time = get_data['check_in_date']
        user_interaction_obj.checkout_date_time = get_data['check_out_date']
        user_interaction_obj.hotel_country = ""
        user_interaction_obj.user_location_country = ""
        user_interaction_obj.user_location_city = ""
        user_interaction_obj.user_location_region = ""
        user_interaction_obj.is_booking = ""
        user_interaction_obj.orig_destination_distance = ""
        user_interaction_obj.srch_destination_id = ""
        user_interaction_obj.srch_adults_cnt = get_data['adults']
        user_interaction_obj.srch_children_cnt = get_data['children']
        user_interaction_obj.srch_rm_cnt = get_data['rooms']


@ csrf_exempt
def index(request):

    place = ""

    if request.GET:

        print(request.GET)
        search_path = request.get_full_path()
        post_data = request.GET
        place = post_data['place']
        checkin_date = post_data['check_in_date']
        checkout_date = post_data['check_out_date']
        rooms = post_data['rooms']
        adults = post_data['adults']
        children = post_data['children']

        page = request.GET.get("page", 1)

        hotels_data_list = HotelDetail.objects.annotate(
            search=SearchVector('district', 'country', 'address'),
        ).filter(search=place)

        paginator = Paginator(list(hotels_data_list), 10)
        try:
            hotels_data = paginator.page(page)
        except PageNotAnInteger:
            hotels_data = paginator.page(1)
        except EmptyPage:
            hotels_data = paginator.page(paginator.num_pages)

        return render(request, "hotel_app/search_result.html", {
            'hotels_data': hotels_data,
        })

    return render(request, "hotel_app/index.html")


def hotel_view(request, hotel_id):

    hotel_data = HotelDetail.objects.get(id=hotel_id)
    print(hotel_data.hotel_name)

    return render(request, "hotel_app/hotel_view.html")
