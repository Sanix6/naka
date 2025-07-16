import random

from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager

class User(AbstractUser):
    username = None
    code = models.IntegerField("Код активации", null=True, blank=True)
    email = models.EmailField('Эл-почта (логин)', unique=True)
    first_name = models.CharField('Имя', max_length=100)
    last_name = models.CharField('Фамилия', max_length=100)
    is_active = models.BooleanField('Активный', default=False)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()


    def save(self, *args, **kwargs):
        self.code = int(random.randint(100_000, 999_999))
        super(User, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
