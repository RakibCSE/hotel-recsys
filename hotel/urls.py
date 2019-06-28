from django.urls import path, re_path

from . import views

app_name = 'hotel'

urlpatterns = [
    path("", views.index, name='index'),
    re_path(r"hotel/(?P<hotel_id>\d+)/", views.hotel_view, name="hotel_view")
]
