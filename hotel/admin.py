from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser, HotelDetail, UserInteraction


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm


admin.site.register(CustomUser, CustomUserAdmin)


class HotelDetailAdmin(admin.ModelAdmin):
    pass


admin.site.register(HotelDetail, HotelDetailAdmin)


class UserInteractionAdmin(admin.ModelAdmin):
    pass


admin.site.register(UserInteraction, UserInteractionAdmin)
