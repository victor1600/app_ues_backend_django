from django.contrib.auth.backends import BaseBackend
from .models import CustomUser as User
from .utils import authenticate


class CustomAuthBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None):
        return authenticate(email=username, password=password)

    def get_user(self, user_id):
        return User.objects.filter(pk=user_id).first()
