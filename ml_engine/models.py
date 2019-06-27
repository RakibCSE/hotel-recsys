from django.db import models


class RecommendedData(models.Model):
    hotel_id = models.CharField(max_length=300)
