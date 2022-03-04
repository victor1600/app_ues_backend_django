from django.dispatch import receiver
from django.conf import settings
from api.signals import *
import logging
import os
from api.models import *

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


@receiver(exam_finished)
def on_exam_finished(sender, **kwargs):
    data = kwargs['data']
    user = kwargs['user']
    if not user.is_anonymous:
        aspirante = Aspirante.objects.filter(user=user).first()
        if aspirante:
            examen = HistoricoExamen.objects.create(aspirante=aspirante, nota=data['grade'])
            logger.info(f'Created exam record for {aspirante} and grade {data["grade"]}')
            for course_name in data.get('partial_grades').keys():
                # TODO: check for possible exception
                course = Curso.objects.filter(texto=course_name).first()
                partial_grade = data.get('partial_grades').get(course_name)
                HistoricoExamenCurso.objects.create(examen=examen, curso=course, nota=partial_grade)
                logger.info(f'Stored partial grade: {partial_grade} for course: {course} for student: {aspirante}')

