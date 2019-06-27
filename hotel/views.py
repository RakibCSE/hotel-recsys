import pandas as pd

from django.shortcuts import render

from .models import HotelDetail
from ml_engine.models import RecommendedData


def index(request):
    recommended_ids = RecommendedData.objects.get(id=1).hotel_id
    id_list = [int(val) for val in recommended_ids.split(",")]
    hotel_details = HotelDetail.objects.filter(hotel_id__in=id_list)

    return render(request, 'hotel_app/index.html', {
        'hotel_details': hotel_details,
    })
