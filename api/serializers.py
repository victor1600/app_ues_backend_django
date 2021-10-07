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
    # TODO: validate there is only one question with is_right_answer set to True.
    class Meta:
        model = Answer
        fields = '__all__'


class ExamQuestionsAndAnswersSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ('id', 'question_text', 'question_image', 'topic',  'answers')


class ExamResultSerializer(serializers.Serializer):
    # TODO: analyze if we really need the questions.
    # question = serializers.PrimaryKeyRelatedField(queryset=Question.objects.all())
    answers = serializers.PrimaryKeyRelatedField(queryset=Answer.objects.all(), many=True)

