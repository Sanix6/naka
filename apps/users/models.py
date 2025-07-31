import random
import uuid


from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager

class User(AbstractUser):
    username = None
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    code = models.IntegerField("Код активации", null=True, blank=True)
    email = models.EmailField('Эл-почта (логин)', unique=True)
    first_name = models.CharField('Имя', max_length=100)
    last_name = models.CharField('Фамилия', max_length=100)
    surname = models.CharField('Отчество', max_length=100, blank=True, null=True)
    phone = models.CharField('Телефон', max_length=15, blank=True, null=True, unique=True)
    avatar = models.ImageField('Аватар', upload_to='avatars/', blank=True)
    birth_date = models.DateField('Дата рождения', blank=True, null=True)
    country = models.CharField('Страна', max_length=100, blank=True, null=True)
    last_activity = models.DateTimeField('Последняя активность', auto_now=True, blank=True, null=True)
    totp_secret = models.CharField(max_length=32, blank=True, null=True)
    is_2fa_enabled = models.BooleanField(default=False)
    phone_verified = models.BooleanField('Телефон подтвержден', default=False)
    is_active = models.BooleanField('Активный', default=False)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()


    def save(self, *args, **kwargs):
        if not self.code:
            self.code = int(random.randint(100_000, 999_999))
        super(User, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class KYCForm(models.Model):
    name = models.CharField(max_length=100) 
    form_id = models.CharField(max_length=64, unique=True)
    is_active = models.BooleanField(default=True)
    description = models.TextField(blank=True)
    target_group = models.CharField(max_length=100, blank=True) 

    def __str__(self):
        return f"{self.name} ({self.form_id})"