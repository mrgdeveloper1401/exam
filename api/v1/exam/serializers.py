from rest_framework import serializers

from accounts.models import User
from exam import models


class ExamCreatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("full_name",)


class ExamSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Exam
        exclude = ("is_deleted", "deleted_at")

    def to_representation(self, instance):
        # super class
        data = super().to_representation(instance)

        # show serializer creator
        data['creator'] = ExamCreatorSerializer(instance.creator).data

        # get obj request
        request = self.context.get("request")

        # check user
        if not request.user.is_staff:
            data.pop("created_at")
            data.pop("updated_at")
        return data


class ExamAttemptSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ExamAttempt
        exclude = ("is_deleted", "deleted_at")
        read_only_fields = ("exam", "user")

    def to_representation(self, instance):
        # super class
        data = super().to_representation(instance)
        # get obj request
        request = self.context.get("request")

        # check user
        if not request.user.is_staff:
            data.pop("created_at", None)
            data.pop("updated_at", None)
            data.pop("user", None)
        return data

    def get_fields(self):
        # super
        field = super().get_fields()

        # get user
        user = self.context.get("request").user

        #check user
        if not user.is_staff:
            field.pop("user", None)
        return field

    def validate(self, attr):
        # get exam pk from urls
        exam_pk = self.context.get('exam_pk')

        # get user id
        user_id = self.context.get('request').user.id

        # filter exam_attempts
        exam_attempts = models.Exam.objects.filter(
            id=exam_pk
        ).only("title")

        # check exam attempts
        if not exam_attempts:
            raise serializers.ValidationError(
                detail={"message": "No exam attempts for this exam."},
                code="not-found"
            )

        # validate unique_together
        if models.ExamAttempt.objects.filter(
            exam_id=exam_pk,
            user_id=user_id
        ).exists():
            raise serializers.ValidationError(
                detail={"message": "Exam attempt already exists for this exam."},
                code="already-exists"
            )

        return attr

    def create(self, validated_data):
        # get exam pk from urls
        exam_pk = self.context.get('exam_pk')

        # get user id from obj request
        request = self.context.get('request')
        user_id = request.user.id
        return models.ExamAttempt.objects.create(
            exam_id=exam_pk,
            user_id=user_id,
            ip_address=request.META.get('REMOTE_ADDR', "X_FORWARDED_FOR")
        )


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Question
        exclude = ("is_deleted", "deleted_at")

    def to_representation(self, instance):
        # super class
        data = super().to_representation(instance)
        # get obj request
        request = self.context.get("request")

        # check user
        if not request.user.is_staff:
            data.pop("created_at", None)
            data.pop("updated_at", None)
            # data.pop("user", None)
        return data
