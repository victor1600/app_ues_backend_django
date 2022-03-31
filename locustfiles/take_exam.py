from locust import HttpUser, task, between
from random import randint
from logging import getLogger

logger = getLogger()


class WebsiteUser(HttpUser):
    wait_time = between(1, 5)

    @task(1)
    def view_topics(self):
        logger.info('[LOAD TEST] Viewing topics')
        # TODO: change this according to actual data.
        course_id = randint(1, 5)
        self.client.get(f'/api/topics/?curso={course_id}', name='/api/topics')

    @task(2)
    def view_topic(self):
        logger.info('[LOAD TEST] Viewing a topic')
        topic_id = randint(1, 5)
        self.client.get(f'/api/topics/{topic_id}',
                        name='/api/topics/:id')

    @task(4)
    def get_exam(self):
        logger.info('[LOAD TEST] Getting exam')
        topic_id = randint(1, 5)
        self.client.get(f'/api/exam-questions/?tema={topic_id}', name='/api/exam-questions/')

    @task(3)
    def calculate_grade(self):
        logger.info('[LOAD TEST] Grading exam')
        answers = [1,8,15]
        self.client.post(f'/api/calculate-grade/',
                         name='/api/calculate-grade/',
                         json={"answers": answers})



