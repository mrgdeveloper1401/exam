from django.contrib import admin

from . import models
# Register your models here.


@admin.register(models.Exam)
class ExamAdmin(admin.ModelAdmin):
    pass


@admin.register(models.UserAnswer)
class UserAnswerAdmin(admin.ModelAdmin):
    pass


@admin.register(models.ExamAttempt)
class ExamAttemptAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Option)
class OptionAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Question)
class QuestionAdmin(admin.ModelAdmin):
    pass
