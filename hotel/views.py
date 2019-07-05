from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.postgres.search import SearchVector
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.edit import CreateView

from .forms import CustomUserCreationForm
from .models import HotelDetail, UserInteraction
from .utils import *

from geoip2 import webservice


class SignUpView(CreateView):
    """
    Sign up view for user signup.
    """
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "signup.html"


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

    user_interaction_obj.hotel_id = query_data.hotel_id
    user_interaction_obj.year = get_year(date_today)
    user_interaction_obj.month = get_month(date_today)
    user_interaction_obj.srch_ci_year = get_year(checkin_date)
    user_interaction_obj.srch_ci_month = get_month(checkin_date)
    user_interaction_obj.srch_co_year = get_year(checkout_date)
    user_interaction_obj.srch_co_month = get_month(checkout_date)
    user_interaction_obj.hotel_country = query_data.country_id
    user_interaction_obj.user_location_country = response.country.geoname_id
    user_interaction_obj.user_location_city = response.city.geoname_id
    user_interaction_obj.user_location_region = response.subdivisions.most_specific.geoname_id
    user_interaction_obj.is_booking = booking
    user_interaction_obj.orig_destination_distance = orig_distance
    user_interaction_obj.srch_destination_id = query_data.district_id
    user_interaction_obj.srch_rm_cnt = room
    user_interaction_obj.srch_adults_cnt = adult
    user_interaction_obj.srch_children_cnt = children
    user_interaction_obj.save()


@ csrf_exempt
def index(request):
    """
    Returns search results view or return to homepage
    Args:
        request:

    Returns:
        request:
        hotel_data: List of queryset.
    """
    if request.GET:
        get_data = request.GET

        request.session['place'] = get_data['place']
        request.session['check_in_date'] = get_data['check_in_date']
        request.session['check_out_date'] = get_data['check_out_date']
        request.session['room'] = get_data['room']
        request.session['adult'] = get_data['adult']
        request.session['children'] = get_data['children']

        place = get_data['place']
        page = int(request.GET.get("page", 1))

        hotels_data_list = HotelDetail.objects.annotate(
            search=SearchVector('hotel_name', 'district', 'country', 'address', 'region'),
        ).filter(search=place)

        paginator = Paginator(list(hotels_data_list), 10)
        # total_pages = paginator.num_pages

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
    """
    Returns hotel view page
    Args:
        request:
        hotel_id: Hotel ID

    Returns:
        request:
        hotel_data: Specific hotel queryset data.
    """

    hotel_data = HotelDetail.objects.get(id=hotel_id)

    # save_search_data(request, hotel_data)

    return render(request, "hotel_app/hotel_view.html", {
        'hotel_data': hotel_data,
    })
