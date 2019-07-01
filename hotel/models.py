from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    username = models.CharField(max_length=25, unique=True)
    email = models.EmailField(unique=True)
    fullname = models.CharField(max_length=100)


class HotelDetail(models.Model):
    hotel_id = models.BigIntegerField()
    accommodation_type = models.TextField(max_length=300)
    hotel_name = models.TextField(max_length=1000)
    address = models.TextField(max_length=1000)
    district = models.TextField(max_length=300)
    region = models.TextField(max_length=50)
    country = models.TextField(max_length=100)
    thumb_urls = models.TextField(max_length=5000)
    star_rating = models.FloatField()
    guest_rating = models.FloatField()
    review_badge = models.TextField(max_length=100)
    hotel_latitude = models.FloatField()
    hotel_longitude = models.FloatField()
    hotel_price = models.TextField(max_length=50)
    district_id = models.IntegerField()
    region_id = models.IntegerField()
    country_id = models.IntegerField()

    def __str__(self):
        return self.hotel_name

    def thumb_urls_as_list(self):
        return self.thumb_urls.split("\n")


class UserInteraction(models.Model):
    user_id = models.BigIntegerField()
    hotel_id = models.BigIntegerField()
    year = models.IntegerField()
    month = models.IntegerField()
    srch_ci_year = models.IntegerField()
    srch_ci_month = models.IntegerField()
    srch_co_year = models.IntegerField()
    srch_co_month = models.IntegerField()
    hotel_country = models.IntegerField()
    user_location_country = models.IntegerField()
    user_location_city = models.IntegerField()
    user_location_region = models.IntegerField()
    is_booking = models.IntegerField()
    orig_destination_distance = models.FloatField()
    srch_destination_id = models.IntegerField()
    srch_adults_cnt = models.IntegerField()
    srch_children_cnt = models.IntegerField()
    srch_rm_cnt = models.IntegerField()

    def __str__(self):
        return self.hotel_id


class CountryData(models.Model):
    country_name = models.CharField(max_length=50)
    country_abbr = models.CharField(max_length=10)
