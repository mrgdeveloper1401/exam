from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import Q

from core.models import ModifyMixin, SoftDeleteMixin
from django.utils.translation import gettext_lazy as _

class Exam(ModifyMixin, SoftDeleteMixin):
    """
    exam model
    """
    title = models.CharField(
        max_length=200,
        help_text=_("Title of the exam (max 200 characters)")
    )
    description = models.TextField(
        verbose_name='توضیحات',
        blank=True,
        help_text=_("Detailed description about the exam")
    )
    creator = models.ForeignKey(
        "accounts.User",
        on_delete=models.PROTECT,
        related_name="exam_creator",
        help_text=_("User who created this exam"),
        limit_choices_to=(Q(is_staff=True) | Q(user_type="teacher") & Q(is_active=True))
    )
    time_limit = models.PositiveIntegerField(
        help_text=_("Exam duration in minutes")
    )
    passing_score = models.PositiveIntegerField(
        help_text=_("Minimum score required to pass the exam (0-100)"),
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='فعال',
        help_text=_("Is this exam currently active and available?")
    )

    class Meta:
        db_table = "exam"
        ordering = ('-created_at',)

    def __str__(self):
        return self.title


class Question(ModifyMixin, SoftDeleteMixin):
    """
    question model
    """
    exam = models.ForeignKey(
        Exam,
        on_delete=models.CASCADE,
        related_name='questions',
        help_text=_("Exam that this question belongs to")
    )
    text = models.TextField(
        help_text=_("Full text of the question")
    )
    image = models.ForeignKey(
        "core.Image",
        on_delete=models.PROTECT,
        help_text=_("Optional image related to the question"),
        null=True,
        blank=True
    )
    score = models.PositiveIntegerField(
        default=1,
        validators=[MinValueValidator(1)],
        help_text=_("Points awarded for correct answer to this question")
    )

    class Meta:
        db_table = "question"

    def __str__(self):
        return f"{self.exam.title}"


class Option(ModifyMixin, SoftDeleteMixin):
    """
    option model
    """
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name='options',
        verbose_name='سوال',
        help_text=_("Question that this option belongs to")
    )
    text = models.CharField(
        max_length=500,
        verbose_name='متن گزینه',
        help_text=_("Text of the option (max 500 characters)")
    )
    is_correct = models.BooleanField(
        default=False,
        verbose_name='پاسخ صحیح',
        help_text=_("Is this the correct answer?")
    )
    # order = models.PositiveIntegerField(
    #     verbose_name='ترتیب نمایش',
    #     default=0,
    #     help_text=_("Display order of this option")
    # )

    class Meta:
        db_table = "option"
        # verbose_name = 'گزینه'
        # verbose_name_plural = 'گزینه‌ها'
        # ordering = ('order',)

    def __str__(self):
        return f"{self.question.text[:30]} - {self.text[:30]}..."


class ExamAttempt(ModifyMixin, SoftDeleteMixin):
    """
    Exam attempt model
    """
    user = models.ForeignKey(
        "accounts.User",
        on_delete=models.CASCADE,
        related_name='exam_attempts',
        help_text=_("User who attempted this exam")
    )
    exam = models.ForeignKey(
        Exam,
        on_delete=models.CASCADE,
        related_name='attempts',
        help_text=_("Exam that was attempted")
    )
    start_time = models.DateTimeField(
        auto_now_add=True,
        help_text=_("When the attempt started")
    )
    end_time = models.DateTimeField(
        null=True,
        blank=True,
        help_text=_("When the attempt was completed")
    )
    score = models.FloatField(
        null=True,
        blank=True,
        help_text=_("Final score of this attempt")
    )
    is_passed = models.BooleanField(
        default=False,
        help_text=_("Did the user pass this attempt?")
    )
    ip_address = models.GenericIPAddressField(
        help_text=_("IP address from which the attempt was made")
    )

    class Meta:
        db_table = "exam_attempt"
        ordering = ('-start_time',)

    def calculate_score(self):
        # محاسبه نمره کاربر
        correct_answers = self.user_answers.filter(
            option__is_correct=True
        ).count()
        total_questions = self.exam.questions.count()
        self.score = (correct_answers / total_questions) * 100 if total_questions else 0
        self.is_passed = self.score >= self.exam.passing_score
        self.save()
        return self.score

    def __str__(self):
        return f"{self.exam.title}"


class UserAnswer(ModifyMixin, SoftDeleteMixin):
    """
    User answer model
    """
    attempt = models.ForeignKey(
        ExamAttempt,
        on_delete=models.CASCADE,
        related_name='user_answers',
        help_text=_("Exam attempt this answer belongs to")
    )
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        help_text=_("Question that was answered")
    )
    option = models.ForeignKey(
        Option,
        on_delete=models.CASCADE,
        verbose_name='گزینه انتخاب شده',
        help_text=_("Option that was selected by the user")
    )
    answered_at = models.DateTimeField(
        auto_now_add=True,
        help_text=_("When this answer was submitted")
    )

    class Meta:
        db_table = "user_answer"
        unique_together = ('attempt', 'question')

    def __str__(self):
        return f"{self.attempt.user.username} - {self.question.text[:30]}"
