from django.dispatch import receiver
from django.conf import settings
from api.signals import test_finished
import logging
import os

logger = logging.getLogger()


@receiver(test_finished)
def on_test_finished(sender, **kwargs):
    """
    This handler will cleanup the media files created by the
    test.
    """
    logger.info("cleaning up media files created by pytest.")
    media_partial_url = kwargs['media_url']
    media_file = os.path.join(settings.BASE_DIR, media_partial_url)
    os.remove(media_file)
    logger.info(f'Deleted {media_file}')

