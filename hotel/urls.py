from django.urls import path, re_path

from . import views
from .views import SignUpView

app_name = 'hotel'

urlpatterns = [
    path("", views.index, name='index'),
    path("accounts/signup/", SignUpView.as_view(), name='signup'),
    re_path(r"hotel/(?P<hotel_id>\d+)/", views.hotel_view, name="hotel_view")
]
