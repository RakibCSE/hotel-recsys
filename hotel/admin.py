from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser, HotelDetail, UserInteraction


class CustomUserAdmin(UserAdmin):
    """
    Custom user details to the admin panel
    """
    model = CustomUser
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(HotelDetail)
admin.site.register(UserInteraction)
