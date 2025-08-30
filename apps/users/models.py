import random
import uuid


from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager
from assets.choices import TYPE_CHOICES

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


class Verification(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE, 
        related_name='verifications'
    )

    type = models.CharField(
        max_length=20,
        choices=TYPE_CHOICES,
        verbose_name="Тип верификации"
    )
    verification_id = models.CharField(
        max_length=100,
        verbose_name="ID верификации",
        null=True, blank=True,
        
    )
    name = models.CharField(
        max_length=100,
        verbose_name="ФИО / Название компании",
        null=True, blank=True
    )
    inn = models.CharField(
        max_length=20,
        verbose_name="ИНН / Регистрационный номер",
        null=True, blank=True
    )
    address = models.CharField(
        max_length=255,
        verbose_name="Адрес регистрации",
        null=True, blank=True
    )
    country = models.CharField(
        max_length=100,
        verbose_name="Страна",
        null=True, blank=True
    )
    is_verified = models.BooleanField(
        null=True, blank=True,
        verbose_name="Статус верификации",
        default=None
    )

    # === Документы ===
    passport_front = models.FileField(
        upload_to="verifications/passports/",
        verbose_name="Паспорт (лицевая сторона)",
        null=True, blank=True
    )
    passport_back = models.FileField(
        upload_to="verifications/passports/",
        verbose_name="Паспорт (оборотная сторона)",
        null=True, blank=True
    )
    registration_doc = models.FileField(
        upload_to="verifications/registration/",
        verbose_name="Скан документа о регистрации",
        null=True, blank=True
    )
    license_doc = models.FileField(
        upload_to="verifications/licenses/",
        verbose_name="Скан лицензии (при наличии)",
        null=True, blank=True
    )
    additional_doc = models.FileField(
        upload_to="verifications/other/",
        verbose_name="Финансовая отчетность / доп. документ",
        null=True, blank=True
    )

    class Meta:
        verbose_name = "Верификация"
        verbose_name_plural = "Верификации"

    def __str__(self):
        return f"{self.name} ({self.get_type_display()})"