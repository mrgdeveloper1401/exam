from datetime import timedelta

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from core.models import SoftDeleteMixin, CreateMixin, ModifyMixin
from .manager import UserManager
from .validation import PhoneNumberValidator
from .validators import unique_email_in_layer_app, unique_nation_code_in_layer_app


class User(AbstractBaseUser, PermissionsMixin, ModifyMixin, SoftDeleteMixin):
    USER_TYPE_CHOICES = (
        ('teacher', 'Teacher'),
        ('student', 'Student'),
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, blank=True, default="student",
                                 help_text=_("The type of user this is. admin - teacher - student"))
    phone_number = models.CharField(unique=True, max_length=15, validators=[PhoneNumberValidator()])
    email = models.EmailField(blank=True, validators=[unique_email_in_layer_app])
    full_name = models.CharField(blank=True, max_length=100)
    nation_code = models.CharField(blank=True, max_length=11, validators=[unique_nation_code_in_layer_app])
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    # is_verify = models.BooleanField(default=False, help_text=_('Is this user verified?'))

    objects = UserManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ('email', "nation_code", "full_name", "user_type")

    def __str__(self):
        return self.phone_number

    class Meta:
        db_table = "auth_user"


class Otp(CreateMixin):
    # TODO, check performance without and have db_index attribute
    # TODO, run otp in redis
    phone_number = models.CharField(validators=[PhoneNumberValidator()], max_length=15, db_index=True)
    otp_code = models.CharField(max_length=8)
    device_ip = models.GenericIPAddressField(blank=True, null=True)
    # is_used = models.BooleanField(default=False, help_text="Is this OTP used?")

    class Meta:
        db_table = "otp"
        ordering = ('-created_at',)

    @property
    def expired_otp(self):
        expired_date = self.created_at + timedelta(minutes=2)
        return expired_date

    @property
    def is_expired(self):
        return self.expired_otp < timezone.now() if self.expired_otp else None


class Student(ModifyMixin, SoftDeleteMixin):
    user = models.OneToOneField(User, on_delete=models.PROTECT, related_name="student")
    student_number = models.CharField(max_length=11, blank=True)
    student_image = models.ForeignKey("core.Image", on_delete=models.DO_NOTHING, related_name="student_image",
                                      null=True, blank=True)
    grade = models.CharField(max_length=20, blank=True)
    parent_phone = models.CharField(unique=True, max_length=15, validators=[PhoneNumberValidator()], blank=True, null=True)

    class Meta:
        db_table = "student"
        ordering = ('-created_at',)
