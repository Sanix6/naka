from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField


class News(models.Model):
    slug = models.SlugField(max_length=255, unique=True, verbose_name='Слаг')
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    image = models.ImageField(upload_to='news_images/', null=True, blank=True, verbose_name='Изображение')
    content = RichTextUploadingField(config_name='default', verbose_name='Контент')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    class Meta:
        verbose_name = ''
        verbose_name_plural = 'Новости'

    def __str__(self):
        return self.title
    
