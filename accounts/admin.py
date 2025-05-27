from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from . import models
# Register your models here.


@admin.register(models.Otp)
class OtpAdmin(admin.ModelAdmin):
    pass


@admin.register(models.User)
class UserAdmin(BaseUserAdmin):
    add_form_template = "admin/auth/user/add_form.html"
    change_user_password_template = None
    fieldsets = (
        (None, {"fields": ("phone_number", "password")}),
        (_("Personal info"), {"fields": ("full_name", "email", "user_type")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "created_at", "updated_at")}),
    )
    list_editable = ("user_type",)
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("phone_number", "user_type", "usable_password", "password1", "password2"),
            },
        ),
    )
    list_display = ("phone_number", "email", "full_name", "user_type", "is_staff", "created_at")
    list_filter = ("is_staff", "is_superuser", "is_active", "groups")
    search_fields = ("phone_number", "full_name", "email")
    ordering = ("-created_at",)
    filter_horizontal = (
        "groups",
        "user_permissions",
    )
    readonly_fields = ("created_at", "updated_at", "last_login")


@admin.register(models.Student)
class StudentAdmin(admin.ModelAdmin):
    pass
