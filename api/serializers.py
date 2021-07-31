from rest_framework import serializers
from .models import Course, SupplementaryMaterial, Question, Topic, Answer


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'


class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = '__all__'


class SupplementaryMaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupplementaryMaterial
        fields = '__all__'


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = '__all__'
