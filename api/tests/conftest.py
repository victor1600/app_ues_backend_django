import pytest
from rest_framework.test import APIClient
from logging import getLogger
from django.contrib.auth.models import User

logger = getLogger()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def authenticate(api_client):
    # TODO: consider adding is super user
    def do_authenticate(is_staff=False):
        return api_client.force_authenticate(user=User(is_staff=is_staff))
    return do_authenticate
