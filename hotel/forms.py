from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    """
    Extends UserCreationForm for custom fields
    """
    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('username', 'email', 'fullname', 'country',)


class CustomUserChangeForm(UserChangeForm):
    """
    Custom user data change form
    """
    class Meta(UserChangeForm):
        model = CustomUser
        fields = UserChangeForm.Meta.fields
