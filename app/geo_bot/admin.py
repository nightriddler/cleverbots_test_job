from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _

from .models import Result, SearchArea, TelegramUser
from .models import User as CustomUser

admin.site.unregister(Group)


class CustomnUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = "__all__"


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    form = CustomnUserChangeForm
    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
        "is_superuser",
        "is_staff",
        "role",
    )
    list_filter = ("role",)

    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "email")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "password1", "password2", "role"),
            },
        ),
    )


@admin.register(SearchArea)
class SearchAreaAdmin(admin.ModelAdmin):
    list_display = ["id", "title"]


@admin.register(TelegramUser)
class TelegramUser(admin.ModelAdmin):
    list_display = ["id", "user_id", "result"]
    list_filter = ("user_id",)


@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ["id", "query", "result", "date"]
