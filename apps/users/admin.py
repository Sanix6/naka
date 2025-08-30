from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Verification
from django.contrib.auth.models import Group
from unfold.admin import ModelAdmin
from django.db import models
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
        "type",
        "name",  
        "country", 
        "is_verified",
        "verification_id"
    )
    list_display_links = list_display
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
            "fields": ("type", "name", "inn", "address", "country", "is_verified")
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
    formfield_overrides = {
        models.BooleanField: {"widget": admin.widgets.AdminRadioSelect}, 
    }
    def user_display(self, obj):
        return obj.user.email   
    user_display.short_description = "Пользователь"



