import pytest
from rest_framework import status
from model_bakery import baker
from api.models import *
from logging import getLogger
import random

logger = getLogger()


@pytest.mark.django_db
class TestExamQuestionFetching:
    def test_exam_grading_returns_correct_grade(self, api_client, authenticate):
        """
        Test if added question and answers are present on the general exam.
        """
        authenticate()
        for _ in range(random.randint(2, 20)):
            question = baker.make(Pregunta, texto='a')
            rand = random.randint(2, 5)
            for i in range(rand):

                if i == rand - 1:
                    print('last question will be the correct one.')
                    es_respuesta_correcta = True
                else:
                    es_respuesta_correcta = False
                baker.make(Respuesta, texto='a', pregunta=question,
                           es_respuesta_correcta=es_respuesta_correcta)

        response = api_client.get(f'/api/exam-questions/?limit=10')
        # get random answer for each question on the sample test.
        answers_objs = [random.choice(q['answers']) for q in response.data]
        id_and_is_right = [(a['id'], a['es_respuesta_correcta']) for a in answers_objs]

        expected_grade = round(
            sum(list(map(lambda x: 1 if x[1] is True else 0, id_and_is_right))) / len(id_and_is_right) * 10, 2)
        print(expected_grade)

        response = api_client.post(f'/api/calculate-grade/', {"answers": [*[e[0] for e in id_and_is_right]]})
        print(response.data['grade'])
        print(response.status_code)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['grade'] == expected_grade
