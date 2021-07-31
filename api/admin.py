from django.contrib import admin
from .models import Course, SupplementaryMaterial, Topic, Answer, Question

# Register your models here.
admin.site.register(Course)
admin.site.register(SupplementaryMaterial)
admin.site.register(Topic)
admin.site.register(Answer)
admin.site.register(Question)
