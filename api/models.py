from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError


def validate_zero_or_one(value):
    if value != 0 or value != 1:
        raise ValidationError("Expected 0 or 1"
                              )


# Create your models here.
class Course(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now=True, blank=True)
    # All images/files get upload to media folder, but here,
    # we define the actual folder well be using inside the media folder.
    icon = models.ImageField(upload_to='photos/icons/%Y/%m/%d/')
    active = models.PositiveSmallIntegerField(default=1)

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
    active = models.PositiveSmallIntegerField(default=1)

    def __str__(self):
        return self.name

    class Meta:
        managed = settings.MANAGED
        db_table = 'TOPICS'


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
        db_table = 'SUPPLEMENTARY_MATERIALS'


class Question(models.Model):
    question_text = models.TextField()
    created_at = models.DateTimeField(auto_now=True, blank=True)
    # TODO: fix this.
    question_image = models.ImageField(upload_to='photos/question_images/%Y/%m/%d/', blank=True)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    active = models.PositiveSmallIntegerField(default=1)

    def __str__(self):
        return self.question_text

    class Meta:
        managed = settings.MANAGED
        db_table = 'QUESTIONS'


class Answer(models.Model):
    answer_text = models.CharField(max_length=400)
    created_at = models.DateTimeField(auto_now=True, blank=True)
    is_right_answer = models.BooleanField()
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    active = models.PositiveSmallIntegerField(default=1, validators=[validate_zero_or_one])

    def __str__(self):
        return self.answer_text

    class Meta:
        managed = settings.MANAGED
        db_table = 'ANSWERS'

