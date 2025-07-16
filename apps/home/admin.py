from django.contrib import admin
from .models import News
from django.utils.html import mark_safe


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):  
    list_display = ['id', 'title', 'get_image_html']
    list_display_links = ['id', 'title']          
    ordering = ['-id']
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}

    fieldsets = (
        ('Основная информация', {'fields': ('title', 'image')}), 
        ('Контент', {'fields': ('slug', 'content')}),
    )

    def get_image_html(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="80" style="object-fit: contain; border: 1px solid #ccc; border-radius: 4px;" />')
        return "—"
    get_image_html.short_description = 'Изображение'
