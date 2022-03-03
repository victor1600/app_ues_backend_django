import sys, os, django
from dotenv import load_dotenv
from logging import getLogger
from django.core.files import File
from utils.exams_loader import load_exam
import base64

from django.core.files.base import ContentFile

load_dotenv()
django_settings_module = os.getenv('DJANGO_SETTINGS_MODULE')

# Path to app_ues_backend_django app
sys.path.append(os.getcwd())
os.environ.setdefault("DJANGO_SETTINGS_MODULE", django_settings_module)
django.setup()

logger = getLogger()


def get_files(path):
    return list(filter(lambda x: '.DS_Store' not in x, os.listdir(path)))


def b64_to_img(img):
    return ContentFile(base64.b64decode(img), name='file.png')


from api.models import *

courses_path = f'data'
for d in get_files(courses_path):
    course, course_created = Curso.objects.get_or_create(texto=d)
    topics_path = f'{courses_path}/{d}'
    for t in get_files(topics_path):
        topic, topic_create = Tema.objects.get_or_create(texto=t, curso=course)
        pdfs_path = f'{topics_path}/{t}/pdf'
        for pdf in get_files(pdfs_path):
            try:
                m, m_created = Material.objects.get_or_create(texto=pdf, archivo=File(open(f'{os.path.join(pdfs_path, pdf)}', 'rb')), tema=topic)
                logger.info(f'Uploaded material to {m.archivo} ')
            except django.db.utils.IntegrityError as e:
                # material already exists
                pass
        exams_path = f'{topics_path}/{t}/exam'
        if 'Algebra' == t:
            exam_files = get_files(exams_path)
            json_exam = list(filter(lambda x: '.json' in x,exam_files))[0]
            txt_exam = list(filter(lambda x: '.txt' in x,exam_files))[0]
            exam = load_exam(f'{exams_path}/{json_exam}', f'{exams_path}/{txt_exam}')
            for i,q in enumerate(exam):
                if 'texto' not in q.keys():
                    # TODO: don't send this to client
                    # TODO: fix this, this might create duplicates as i could change.
                    q['texto'] = f'autogenerado_{topic}_{i+1}'

                if 'imagen' in q.keys():
                    q['imagen'] = b64_to_img(q.get('imagen'))

                answers = q.pop('answers')

                try:
                    question, q_created = Pregunta.objects.get_or_create(**q, tema=topic)
                    if q_created:
                        logger.info(f'Created question for {topic}')
                except django.db.utils.IntegrityError:
                    pass

                for y, a in enumerate(answers):
                    if 'imagen' in a.keys():
                        a['imagen'] = b64_to_img(a.get('imagen'))

                    # if 'texto' not in a.keys():
                    #     # TODO: don't send this to client
                    #     # TODO: fix this, this might create duplicates as i could change.
                    if 'texto' not in a.keys():
                        a['texto'] = f'autogenerado_{question.id}_{a["literal"]}'
                    try:
                        Respuesta.objects.get_or_create(**a, pregunta=question)
                    except django.db.utils.IntegrityError as e:
                        pass





