from rest_framework_nested import routers

from . import views

app_name = "v1_exam"

router = routers.SimpleRouter()
router.register(r'exams', views.ExamViewSet, basename='exam')

exam_router = routers.NestedSimpleRouter(router, r'exams', lookup='exam')
exam_router.register("exam_attempts", views.ExamAttemptViewSet, basename='exam_attempt')
exam_router.register("questions", views.QuestionViewSet, basename='question')

urlpatterns = [] + router.urls + exam_router.urls
