from rest_framework import viewsets, permissions

from . import serializers
from exam import models
from ..utils.pagination import CommonPageNumberPagination


class ExamViewSet(viewsets.ModelViewSet):
    queryset = models.Exam.objects.defer(
        "is_deleted", "deleted_at"
    )
    serializer_class = serializers.ExamSerializer
    pagination_class = CommonPageNumberPagination

    def get_permissions(self):
        if self.request.method in ('GET', 'HEAD', 'OPTIONS'):
            self.permission_classes = (permissions.AllowAny,)
        else:
            self.permission_classes = (permissions.IsAdminUser,)
        return super().get_permissions()



class ExamAttemptViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ExamAttemptSerializer
    pagination_class = CommonPageNumberPagination

    def get_queryset(self):
        return models.ExamAttempt.objects.defer(
        "is_deleted", "deleted_at"
    ).filter(
            exam_id=self.kwargs["exam_id"],
        )

    def get_permissions(self):
        if self.request.method in ("PUT", "PATCH", 'DELETE'):
            self.permission_classes = (permissions.IsAdminUser,)
        else:
            self.permission_classes = (permissions.IsAuthenticated,)
        return super().get_permissions()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['exam_pk'] = self.kwargs.get('exam_pk')
        return context


class QuestionViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.QuestionSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_permissions(self):
        if self.request.method not in permissions.SAFE_METHODS:
            self.permission_classes = (permissions.IsAdminUser,)
        return super().get_permissions()

    def get_queryset(self):
        return models.Question.objects.filter(
            exam_id=self.kwargs.get("exam_pk"),
        ).defer(
            "is_deleted", "deleted_at"
        )
