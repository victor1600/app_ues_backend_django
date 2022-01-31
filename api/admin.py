from django.contrib import admin
from .models import Course, SupplementaryMaterial, Topic, Answer, Question
from django.db.models.aggregates import Count
from django.utils.html import format_html, urlencode
from django.urls import reverse

# Register your models here.

admin.site.register(SupplementaryMaterial)
# admin.site.register(Topic)
admin.site.register(Answer)
admin.site.register(Question)


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'created_at', 'topics_count']

    @admin.display(ordering='topics_count')
    def topics_count(self, course):
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
    list_display = ['name', 'created_at', 'course_name']
    list_select_related = ['course']

    def course_name(self, topic):
        # Connect to parent
        url = reverse('admin:api_course_change', args=(topic.course.id,))
        return format_html('<a href="{}">{}</a>', url, topic.course.name)

