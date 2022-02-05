from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """
    Extension of AbstractUser to add extra data of the user
    """
    username = models.CharField(max_length=25, unique=True)
    email = models.EmailField(unique=True)
    fullname = models.CharField(max_length=100)
    country = models.CharField(max_length=30, default="")


class HotelDetail(models.Model):
    """
    Hotel details table
    """
    hotel_id = models.BigIntegerField()
    accommodation_type = models.CharField(max_length=20)
    hotel_name = models.CharField(max_length=200)
    address = models.CharField(max_length=300, null=True)
    district = models.CharField(max_length=30, null=True)
    region = models.CharField(max_length=50, null=True)
    country = models.CharField(max_length=100)
    thumb_urls = models.CharField(max_length=5000, null=True)
    star_rating = models.FloatField(null=True)
    guest_rating = models.FloatField(null=True)
    review_badge = models.CharField(max_length=30, null=True)
    hotel_latitude = models.FloatField(null=True)
    hotel_longitude = models.FloatField(null=True)
    hotel_price = models.CharField(max_length=50)
    district_id = models.IntegerField()
    region_id = models.IntegerField()
    country_id = models.IntegerField()
    cluster = models.IntegerField(default=0)

    def __str__(self):
        return self.hotel_name

    def thumb_urls_as_list(self):
        """
        Returns:
            urls_list: Urls list of the thumb urls of the hotel pictures.
        """
        urls_list = self.thumb_urls.split("\n")
        return urls_list

    def star_as_integer(self):
        """
        Returns:
            star_rating: Returns star rating.
        """
        star_rating = float(self.star_rating) * 20
        return int(star_rating)

    def format_price(self):
        """
        Returns:
            formatted_price: Returns formatted price of the hotels.
        """
        formatted_price = "{}{}".format("$", self.hotel_price.lstrip("USD"))
        return formatted_price


class UserInteraction(models.Model):
    """
    User interaction model to save user interaction data
    """
    user_id = models.BigIntegerField()
    hotel_id = models.BigIntegerField()
    date_time_year = models.IntegerField()
    date_time_month = models.IntegerField()
    srch_ci_year = models.IntegerField()
    srch_ci_month = models.IntegerField()
    srch_co_year = models.IntegerField()
    srch_co_month = models.IntegerField()
    is_booking = models.IntegerField(default=0)
    hotel_country = models.IntegerField()
    user_location_country = models.IntegerField()
    user_location_city = models.IntegerField()
    user_location_region = models.IntegerField()
    orig_destination_distance = models.FloatField()
    srch_destination_id = models.IntegerField()
    srch_adults_cnt = models.IntegerField()
    srch_children_cnt = models.IntegerField()
    srch_rm_cnt = models.IntegerField()
    hotel_cluster = models.IntegerField(default=0)

    def __str__(self):
        return str(self.hotel_id)


class UserSearch(models.Model):
    """
    User search model to save search keywords
    """
    keyword = models.CharField(max_length=200)
    hotel_id = models.BigIntegerField()
    hotel_cluster = models.IntegerField(default=0)
    counter = models.PositiveIntegerField(default=0)

    def __str__(self):
        return str(f'{self.keyword}|{self.counter}')
