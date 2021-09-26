from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
# TODO: register viewset
router.register(r'courses', views.CourseViewSet)
router.register(r'topics', views.TopicViewSet)
router.register(r'materials', views.SupplementaryMaterialViewSet)
router.register(r'questions', views.QuestionViewSet)
router.register(r'answers', views.AnswerViewSet)
router.register(r'exam-questions', views.ExamQuestionsAndAnswersViewSet)

urlpatterns = [
    path('', include(router.urls)),
    # path('auth/', include('rest_auth.urls')),
]
