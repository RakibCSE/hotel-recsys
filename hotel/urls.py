from django.urls import path

from . import views

app_name = 'hotel'

urlpatterns = [
    path("", views.index, name='index'),
]
