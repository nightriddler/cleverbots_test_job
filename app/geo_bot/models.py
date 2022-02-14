from django.contrib.auth.models import AbstractUser, Permission
from django.db import models
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from django_tg_bot.settings import DESCRIPTION_ROLE, USER_ROLE_PERMISSIONS


class User(AbstractUser):
    ROLE_CHOICES = [("user", "Пользователь"), ("moderator", "Модератор")]
    role = models.CharField(
        max_length=250,
        verbose_name="Роль пользователя",
        help_text=DESCRIPTION_ROLE,
        choices=ROLE_CHOICES,
    )


@receiver(pre_save, sender=User)
def prepare_creat_user_profile(sender, instance, **kwargs):
    instance.is_staff = True


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created and instance.role:
        instance.user_permissions.set(
            [
                Permission.objects.get(codename=perm)
                for perm in USER_ROLE_PERMISSIONS[instance.role]
            ]
        )


class TelegramUser(models.Model):
    user_id = models.CharField(max_length=250, verbose_name="CHAT_ID пользователя")
    result = models.ForeignKey(
        "Result", on_delete=models.CASCADE, blank=False, verbose_name="Результаты"
    )

    class Meta:
        verbose_name = "Пользователь бота"
        verbose_name_plural = "Пользователи бота"

    def __str__(self):
        return f"{self.user_id} -> {self.result}"


class SearchArea(models.Model):
    title = models.CharField(max_length=250, verbose_name="Название")

    class Meta:
        verbose_name = "Область поиска"
        verbose_name_plural = "Области поиска"

    def __str__(self):
        return self.title


class Result(models.Model):
    query = models.CharField(max_length=250, verbose_name="Запрос")
    result = models.CharField(max_length=250, verbose_name="Результат")
    date = models.DateField(auto_now_add=True, verbose_name="Дата запроса")

    class Meta:
        verbose_name = "Результат поиска"
        verbose_name_plural = "Результаты поиска"

    def __str__(self):
        return f"{self.query} -> {self.result} ({self.date.strftime('%d.%m.%Y')})"
