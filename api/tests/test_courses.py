from io import StringIO

from django.conf import settings
from rest_framework.test import APIClient
from rest_framework import status

from PIL import Image
import pytest


@pytest.mark.django_db
class TestCreateCourse:
    def test_if_user_is_anonymous_returns_401(self):
        client = APIClient()
        # TODO: Create test for uploading an image.
        response = client.post('/api/courses/', {'texto': 'a',
                                                 'icono': open(f'{settings.BASE_DIR}/icons/biologia.png', 'rb')})

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
