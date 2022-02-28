import sys, os, django
from dotenv import load_dotenv
from logging import getLogger
from django.core.files import File


load_dotenv()
django_settings_module = os.getenv('DJANGO_SETTINGS_MODULE')

# Path to app_ues_backend_django app
sys.path.append(os.getcwd())
os.environ.setdefault("DJANGO_SETTINGS_MODULE", django_settings_module)
django.setup()

logger = getLogger()


def get_files(path):
    return list(filter(lambda x: '.DS_Store' not in x, os.listdir(path)))


from api.models import *

courses_path = f'data'
for d in get_files(courses_path):
    course = Curso.objects.get(texto=d)
    topics_path = f'{courses_path}/{d}'
    for t in get_files(topics_path):
        topic = Tema.objects.create(texto=t, curso=course)
        pdfs_path = f'{topics_path}/{t}/pdf'
        for pdf in get_files(pdfs_path):
            m = Material.objects.create(texto=pdf, archivo=File(open(f'{os.path.join(pdfs_path, pdf)}', 'rb')), tema=topic)
            logger.info(f'Uploaded material to {m.archivo} ')


