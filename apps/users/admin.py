from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Verification
from django.contrib.auth.models import Group
from unfold.admin import ModelAdmin
from django.db import models
from django.utils.html import format_html

admin.site.unregister(Group)


@admin.register(User)
class UserAdmin(UserAdmin):
    list_display = ['id', 'email', 'first_name', 'last_name']
    list_display_links = ['id', 'email', 'first_name', 'last_name']
    ordering = ['-id']
    fieldsets = (
        ('Основаная информация', {'fields': ('email', 'first_name','last_name', 'phone', 'birth_date', 'country')}),
        ('Права', {'fields': ('is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Важные даты', {'fields': ('last_login', 'date_joined')}),
        ('Активация', {'fields': ('is_active', 'phone_verified', 'code')}))


@admin.register(Verification)
class VerificationAdmin(admin.ModelAdmin):
    list_display = (
        "id", 
        "user_display",
        "colored_type",   
        "name",  
        "country", 
        "is_verified",
        "verification_id"
    )
    list_display_links = ("id", "user_display", "name")
    list_filter = (
        "type",      
        "is_verified",
        "country",    
    )
    search_fields = (
        "name", 
        "inn", 
        "address"
    )
    
    ordering = ("-id",)  
    list_per_page = 20  

    fieldsets = (
        ("Основная информация", {
            "fields": ("is_verified", "type", "name", "inn", "address", "country")
        }),
        ("Документы", {
            "fields": (
                "passport_front",
                "passport_back",
                "registration_doc",
                "license_doc",
                "additional_doc",
            )
        }),
    )

    def user_display(self, obj):
        return obj.user.email   
    user_display.short_description = "Пользователь"

    def colored_type(self, obj):
        colors = {
            "personal": "#2196f3",  
            "company": "#4caf50",  
            "license": "#ff9800",   
        }
        return format_html(
            '<span style="display:inline-block; padding:4px 10px; '
            'font-size:12px; font-weight:500; color:white; '
            'background-color:{}; border-radius:4px; '
            'box-shadow:0 1px 2px rgba(0,0,0,0.15);">'
            '{}</span>',
            colors.get(obj.type, "gray"),
            obj.get_type_display() if hasattr(obj, "get_type_display") else obj.type
        )
    colored_type.short_description = "Тип"

