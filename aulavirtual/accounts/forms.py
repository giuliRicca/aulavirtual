from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import UserManage


class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = UserManage
        fields = ('email',)


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = UserManage
        fields = ('email',)
