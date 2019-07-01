from django.contrib import admin

from .models import RecommendedData


class RecommendedDataAdmin(admin.ModelAdmin):
    pass


admin.site.register(RecommendedData, RecommendedDataAdmin)
