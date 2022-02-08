from django.dispatch import receiver
from api.signals import test_finished
import logging

logger = logging.getLogger()


@receiver(test_finished)
def on_test_finished(sender, **kwargs):
    logger.info("cleaning up media files created by pytest.")
    media_url = kwargs['media_url']
    # TODO: to this media url, append base dir:
    #  media/photos/icons/2022/02/08/biologia_1fBIIV4.png

    # TODO: Delete media path.
    logger.info(media_url)
