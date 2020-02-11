import json
import pandas as pd
import logging

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.db.models import Q
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.edit import CreateView

from .forms import CustomUserCreationForm
from .models import HotelDetail, UserInteraction
from . import utils


logger = logging.getLogger("views")


class SignUpView(CreateView):
    """
    Sign up view for user signup.
    """
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "accounts/signup.html"


@csrf_exempt
def index(request):
    """
    Returns search results view or return to homepage
    Args:
        request:

    Returns:
        response:
    """

    utils.train_algorithm()

    response = render(request, "hotel_app/index.html", {
        'session': request.session
    })
    return response


def hotel_view(request, hotel_id):
    """
    Returns hotel view page
    Args:
        request:
        hotel_id: Hotel ID

    Returns:
        response: Response with hotel data
    """

    hotel_data = HotelDetail.objects.get(id=int(hotel_id))

    utils.save_search_data(request, hotel_data, booking=0)

    response = render(request, "hotel_app/hotel_view.html", {
        'hotel_data': hotel_data,
        'session': request.session
    })
    return response


@login_required
def book(request, hotel_id):
    """
    Book hotel
    Args:
        request:
        hotel_id:

    Returns:
        response:
    """
    if request.POST:
        post_data = request.POST

        request.session['hotel_name'] = post_data['hotel_name']
        request.session['check_in_date'] = post_data['check_in_date']
        request.session['check_out_date'] = post_data['check_out_date']
        request.session['room'] = post_data['room']
        request.session['room'] = post_data['room']
        request.session['adult'] = post_data['adult']
        request.session['children'] = post_data['children']

        hotel_data = HotelDetail.objects.get(id=int(hotel_id))
        utils.save_search_data(request, hotel_data, booking=1)

        response = render(request, "hotel_app/index.html", {
            'message': "Hotel booked successfully."
        })

        return response

    response = render(request, "hotel_app/index.html", {
        'message': "Something wrong. Try again."
    })
    return response


def search_by_query(query_text):
    """
    Returns query results as a queryset.

    Args:
        query_text (str): Search query text

    Returns:
        query_result: Query result
    """
    vector = SearchVector('accommodation_type', 'hotel_name',
                          'district', 'country', 'address', 'region', 'review_badge',)
    query = SearchQuery(query_text)
    query_result = HotelDetail.objects.annotate(
        search=vector).filter(search=query)
    return query_result


def search(request):
    """
    Returns the search results
    Args:
        request: GET request with search parameters

    Returns:
        response:
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

        hotels_data_list = search_by_query(place)

        paginator = Paginator(list(hotels_data_list), 10)

        # Recommendation section
        recommended_hotels = []
        hotel_clusters = utils.get_recommendations(request, hotels_data_list)

        districts = list(set([data["district_id"]
                              for data in list(hotels_data_list.values())]))

        if hotel_clusters and districts:
            recommended_hotels = HotelDetail.objects.filter(
                cluster__in=hotel_clusters, district_id__in=districts)

        try:
            hotels_data = paginator.page(page)
        except PageNotAnInteger:
            hotels_data = paginator.page(1)
        except EmptyPage:
            hotels_data = paginator.page(paginator.num_pages)

        response = render(request, "hotel_app/search_result.html", {
            'hotels_data': hotels_data,
            'recommended_hotels': recommended_hotels[:5],
            'session': request.session
        })
        return response

    response = render(request, "hotel_app/search_result.html", {
        'session': request.session
    })
    return response


def search_ajax(request):
    """
    Returns AJAX Search results
    Args:
        request:

    Returns:
        JsonResponse: Return search data into JSON
    """
    search_data = {}
    if request.is_ajax:
        place_text = request.GET['place_text']

        hotels_data_list = search_by_query(place_text)

        hotel_data_df = pd.DataFrame(list(hotels_data_list.values())).dropna()

        if not hotel_data_df.empty:

            country_list = hotel_data_df.country.unique().tolist()
            location_list = hotel_data_df.region.unique().tolist() + hotel_data_df.district.unique().tolist()
            hotel_list = hotel_data_df.hotel_name.unique().tolist()

            search_data_json = json.dumps({
                "country_result": {
                    "heading": "Country",
                    "result": country_list
                },
                "location_result": {
                    "heading": "Places",
                    "result": location_list
                },
                "hotel_result": {
                    "heading": "Hotels",
                    "result": hotel_list
                }
            })

            return JsonResponse(search_data_json, safe=False)
        else:
            return JsonResponse(json.dumps({
                "status": "No data found",
            }), safe=False)
