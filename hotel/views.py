import pandas as pd

from django.shortcuts import render
from django.contrib.postgres.search import SearchVector

from .models import HotelDetail
from ml_engine.models import RecommendedData


def index(request):
    if request.POST:
        post_data = request.POST
        place = post_data['place']
        checkin_date = post_data['check_in_date']
        checkout_date = post_data['check_out_date']
        guest = post_data['guests']

        hotels_data = HotelDetail.objects.annotate(
            search=SearchVector('district', 'country', 'address'),
        ).filter(search=place)

        # results = BlogPost.objects.annotate(
        #     search=SearchVector('title', 'intro', 'content'),
        # ).filter(search=your_search_query)

        print(place)
        print(checkin_date)
        print(checkout_date)
        print(guest)

        return render(request, "hotel_app/search_result.html", {
            'hotels_data': hotels_data
        })

    return render(request, "hotel_app/index.html")
