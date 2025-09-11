from django.contrib import admin
from .models import Finance, Rates, HistoryTransactions
from unfold.admin import ModelAdmin
from django.utils.html import mark_safe
from django.utils.html import format_html
import re

@admin.register(Finance)
class FinanceAdmin(admin.ModelAdmin):
    list_display = (
        'logo_display','name', 'currency', 'network', 'decimal',
        'min_amount', 'max_amount',
        'status_buy', 'status_sell', 'fee', 
    )
    actions = ['delete_selected'] 
    list_display_links = list_display
    search_fields = ('name', 'currency')
    list_filter = ('status_buy', 'status_sell')

    def logo_display(self, obj):
        if obj.logo:
            return mark_safe(f'<img src="{obj.logo.url}" width="50" height="50" />')
        return "Нет лого"
    logo_display.short_description = 'Логотип'



@admin.register(Rates)
class RatesAdmin(admin.ModelAdmin):
    list_display = ('get_currency_from', 'get_currency_to', 'rate', 'fixed', 'updated_at')
    search_fields = ('currency_f__currency', 'currency_t__currency')
    list_display_links = list_display

    def get_currency_from(self, obj):
        return format_html(
            '<span style="display:inline-block; padding:6px 12px; '
            'font-size:14px; font-weight:500; color:#fff; '
            'background-color:#EE4B2B; border-radius:2px; '
            'text-align:center; width:120px; text-transform: uppercase;">{}</span>'
            '<span style="display:inline-block; font-size:12px; color:#fff; margin-left:10px; '
            'background-color:#EE4B2B; border-radius:2px; padding:2px 6px;">{}</span>',
            obj.currency_f.currency, obj.currency_f.network
        )
    get_currency_from.short_description = 'From'

    def get_currency_to(self, obj):
        return format_html(
            '<span style="display:inline-block; padding:6px 12px; '
            'font-size:14px; font-weight:500; color:#fff; '
            'background-color:#4caf50; border-radius:2px; '
            'text-align:center; width:120px; text-transform: uppercase;">{}</span>'
            '<span style="display:inline-block; font-size:12px; color:#fff; margin-left:10px; '
            'background-color:#4caf50; border-radius:2px; padding:2px 6px;">{}</span>',
            obj.currency_t.currency, obj.currency_t.network
        )
    get_currency_to.short_description = 'To'





@admin.register(HistoryTransactions)
class HistoryTransactionsAdmin(admin.ModelAdmin):
    list_display = (
        "currency_from_display",
        "amount_from_display",
        "currency_to_display",
        "amount_to_display",
        "colored_status",
        "colored_type_of_change",
        "rate",
        "fee",
        "application_id",
        "created_at",
        "user",
    )
    search_fields = ("user__email", "currency_from__currency", "currency_to__currency")
    list_filter = ("user", "currency_from", "currency_to", "status", "created_at", "type_of_change")
    date_hierarchy = "created_at"
    ordering = ("-created_at",)
    list_display_links = list_display
    

    def currency_from_display(self, obj):
        if obj.currency_from and obj.currency_from.logo and obj.currency_from.logo.url:
            return format_html(
                '<span style="display:flex;align-items:center;gap:6px;">'
                '<img src="{}" width="20" height="20" style="border-radius:50%;object-fit:cover;" />'
                '<span style="font-weight:600;color:#f44336;">{}</span>'
                '</span>',
                obj.currency_from.logo.url,
                obj.currency_from.currency
            )
        return obj.currency_from.currency if obj.currency_from else "-"
    currency_from_display.short_description = "Списание"

    def currency_to_display(self, obj):
        if obj.currency_to and obj.currency_to.logo and obj.currency_to.logo.url:
            return format_html(
                '<span style="display:flex;align-items:center;gap:6px;">'
                '<img src="{}" width="20" height="20" style="border-radius:50%;object-fit:cover;" />'
                '<span style="font-weight:600;color:#4caf50;">{}</span>'
                '</span>',
                obj.currency_to.logo.url,
                obj.currency_to.currency
            )
        return obj.currency_to.currency if obj.currency_to else "-"
    currency_to_display.short_description = "Зачисление"

    def amount_from_display(self, obj):
        if obj.amount_from is not None:
            value = f"{float(obj.amount_from):.2f}"
            return format_html(
                '<span style="font-weight:600; color:#f44336;">{}</span>',
                value
            )
        return "-"
    amount_from_display.short_description = "Сумма списания"

    def amount_to_display(self, obj):
        if obj.amount_to is not None:
            value = f"{float(obj.amount_to):.2f}"
            return format_html(
                '<span style="font-weight:600; color:#4caf50;">{}</span>',
                value
            )
        return "-"
    amount_to_display.short_description = "Сумма зачисления"

    def colored_status(self, obj):
        colors = {
            "1": "#2196f3",  # В ожидании
            "2": "#ff9800",  # Ожидание
            "3": "#D100D1",  # Обработка
            "4": "#D10000",  # Отменено
            "5": "#4caf50",  # Завершено
        }
        return format_html(
            '<span style="display:inline-block; padding:6px 12px; '
            'font-size:12px; font-weight:500; color:white; '
            'background-color:{}; border-radius:4px; '
            'box-shadow:0 1px 2px rgba(0,0,0,0.15);">'
            '{}</span>',
            colors.get(obj.status, "#9e9e9e"), 
            obj.get_status_display() if obj.status else "Unknown"
        )

    colored_status.short_description = "Статус"
    
    def colored_type_of_change(self, obj):
        colors = {
            "1": "#ff9800",  
            "2": "#4caf50",  
        }
        
        status_display = obj.get_type_of_change_display() if obj.type_of_change else "Unknown"
        
        status_display_cleaned = re.sub(r'\d+', '', status_display)
        
        return format_html(
            '<span style="display:inline-block; padding:6px 12px; '
            'font-size:12px; font-weight:500; color:white; '
            'background-color:{}; border-radius:4px; '
            'box-shadow:0 1px 2px rgba(0,0,0,0.15);">'
            '{} </span>',
            colors.get(obj.type_of_change, "#9e9e9e"),
            status_display_cleaned
        )
    colored_type_of_change.short_description = "Тип заявки"
