from django.db import models
from django.conf import settings


# Create your models here.
class Course(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now=True, blank=True)
    # All images/files get upload to media folder, but here,
    # we define the actual folder well be using inside the media folder.
    icon = models.ImageField(upload_to='photos/icons/%Y/%m/%d/')
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        managed = settings.MANAGED
        db_table = 'COURSES'


class Topic(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now=True, blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class SupplementaryMaterial(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now=True, blank=True)
    file = models.FileField(upload_to='files/%Y/%m/%d/')
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        managed = settings.MANAGED
        db_table = 'SUPPLEMENTARY_MATERIAL'


class Question(models.Model):
    question_text = models.TextField()
    created_at = models.DateTimeField(auto_now=True, blank=True)
    question_image = models.ImageField(upload_to='photos/question_images/%Y/%m/%d/', blank=True)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.question_text


class Answer(models.Model):
    answer_text = models.CharField(max_length=400)
    created_at = models.DateTimeField(auto_now=True, blank=True)
    is_right_answer = models.BooleanField()
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.answer_text
