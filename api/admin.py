from django.contrib import admin
from .models import Course, Material, Topic, Answer, Question
from django.db.models.aggregates import Count
from django.utils.html import format_html, urlencode
from django.urls import reverse

# Register your models here.

admin.site.register(Material)
# admin.site.register(Topic)
admin.site.register(Answer)


# admin.site.register(Question)


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'created_at', 'temas_por_materia']

    @admin.display(ordering='topics_count')
    def temas_por_materia(self, course):
        # Connect to children
        url = (
                reverse('admin:api_topic_changelist')
                + '?'
                + urlencode({
            'course__id': str(course.id)
        }))
        if course.topics_count == 0:
            return course.topics_count
        else:
            return format_html('<a href="{}">{}</a>', url, course.topics_count)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            topics_count=Count('topic')
        )


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at', 'curso', 'preguntas_por_tema', 'materiales_por_tema']
    list_select_related = ['course']

    def curso(self, topic):
        # Connect to parent
        url = reverse('admin:api_course_change', args=(topic.course.id,))
        return format_html('<a href="{}">{}</a>', url, topic.course.name)

    @admin.display(ordering='questions_count')
    def preguntas_por_tema(self, topic):
        # Connect to children
        url = (
                reverse('admin:api_question_changelist')
                + '?'
                + urlencode({
            'topic__id': str(topic.id)
        }))
        if topic.questions_count == 0:
            return topic.questions_count
        else:
            return format_html('<a href="{}">{}</a>', url, topic.questions_count)

    @admin.display(ordering='material_count')
    def materiales_por_tema(self, topic):
        url = (
                reverse('admin:material_changelist')
                + '?'
                + urlencode({
            'topic__id': str(topic.id)
        }))
        if topic.material_count == 0:
            return topic.material_count
        else:
            return format_html('<a href="{}">{}</a>', url, topic.material_count)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            questions_count=Count('question'),
            material_count=Count('material')
        )


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['question_text', 'tema']
    list_select_related = ['topic']

    def tema(self, question):
        url = reverse('admin:api_topic_change', args=(question.topic.id,))
        return format_html('<a href="{}">{}</a>', url, question.topic.name)
