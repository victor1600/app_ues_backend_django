from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
# TODO: register viewset
router.register(r'courses', views.CourseViewSet)
router.register(r'topics', views.TopicViewSet)
router.register(r'materials', views.MaterialViewSet)
router.register(r'questions', views.QuestionViewSet)
router.register(r'answers', views.AnswerViewSet)
router.register(r'exam-questions', views.ExamQuestionsAndAnswersViewSet)
router.register(r'aspirantes', views.CandidateApiViewSet)
router.register(r'rules', views.RulesViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('calculate-grade/', views.GradeView.as_view()),
]
