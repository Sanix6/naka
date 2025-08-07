from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from apps.users.models import User

class News(models.Model):
    slug = models.SlugField(max_length=255, unique=True, verbose_name='Слаг')
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    image = models.ImageField(upload_to='news_images/', null=True, blank=True, verbose_name='Изображение')
    content = RichTextUploadingField(config_name='default', verbose_name='Контент')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    url = models.URLField(max_length=255, null=True, blank=True, verbose_name='Ссылка')

    class Meta:
        verbose_name = ''
        verbose_name_plural = 'Новости'

    def __str__(self):
        return self.title
    

class FeedBack(models.Model):
    name = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    star = models.IntegerField(default=0, null=True, blank=True, verbose_name='Оценка')
    text = models.TextField(verbose_name='Сообщение')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    class Meta:
        verbose_name = 'Обратная связь'
        verbose_name_plural = 'Обратная связь'

    def __str__(self):
        return str(self.name)


class FAQ(models.Model):
    question = models.CharField(max_length=255, verbose_name='Вопрос')
    answer = models.TextField(verbose_name='Ответ')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    class Meta:
        verbose_name = 'Часто задаваемый вопрос'
        verbose_name_plural = 'Часто задаваемые вопросы'

    def __str__(self):
        return self.question