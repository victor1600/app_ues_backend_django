from io import StringIO
import logging
from django.conf import settings
from rest_framework.test import APIClient
from rest_framework import status
from api.signals import test_finished

import pytest

logger = logging.getLogger()


@pytest.mark.django_db
class TestCreateCourse:
    def test_if_user_is_anonymous_returns_401(self):
        client = APIClient()
        # TODO: Create test for uploading an image.
        image_url = f'{settings.BASE_DIR}/icons/biologia.png'
        response = client.post('/api/courses/', {'texto': 'a',
                                                 'icono': open(image_url, 'rb')})
        logger.info(response.data)
        # We can supply additional data using **kwargs
        if 'icono' in response.data:
            media_url_partial_path = response.data['icono'].split("testserver/")[1]
            test_finished.send_robust(sender=self.__class__, media_url=media_url_partial_path)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

