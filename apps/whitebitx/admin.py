from django.contrib import admin
from .models import Finance, Rates, HistoryTransactions
from unfold.admin import ModelAdmin
from django.utils.html import mark_safe
from django.utils.html import format_html


@admin.register(Finance)
class FinanceAdmin(admin.ModelAdmin):
    list_display = (
        'logo_display','name', 'currency', 'network', 'decimal',
        'min_amount', 'max_amount',
        'status_buy', 'status_sell', 'sell_fee', 'buy_fee', 
    )
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

    def get_currency_from(self, obj):
        return format_html(
            '<span style="display:inline-block; padding:2px 8px; '
            'font-size:12px; font-weight:600; color:white; '
            'background-color:#2196f3; border-radius:6px;">{}</span>',
            obj.currency_f.currency
        )
    get_currency_from.short_description = 'From'

    def get_currency_to(self, obj):
        return format_html(
            '<span style="display:inline-block; padding:2px 8px; '
            'font-size:12px; font-weight:600; color:white; '
            'background-color:#4caf50; border-radius:6px;">{}</span>',
            obj.currency_t.currency
        )
    get_currency_to.short_description = 'To'

@admin.register(HistoryTransactions)
class HistoryTransactionsAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "currency_from_display",
        "amount_from_display",
        "currency_to_display",
        "amount_to_display",
        "rate",
        "fee",
        "colored_status",
        "created_at",
        "type_of_change",
        "application_id"
    )
    search_fields = ("user__email", "currency_from__currency", "currency_to__currency")
    list_filter = ("user", "currency_from", "currency_to", "status", "created_at", "type_of_change")
    date_hierarchy = "created_at"
    ordering = ("-created_at",)
    list_display_links = list_display

    def currency_from_display(self, obj):
        if obj.currency_from.logo:
            return format_html(
                '<span style="display:flex;align-items:center;gap:6px;">'
                '<img src="{}" width="20" height="20" style="border-radius:50%;object-fit:cover;" />'
                '<span style="font-weight:600;color:#f44336;">{}</span>'
                '</span>',
                obj.currency_from.logo.url,
                obj.currency_from.currency
            )
        return obj.currency_from.currency
    currency_from_display.short_description = "Списание"

    def currency_to_display(self, obj):
        if obj.currency_to.logo:
            return format_html(
                '<span style="display:flex;align-items:center;gap:6px;">'
                '<img src="{}" width="20" height="20" style="border-radius:50%;object-fit:cover;" />'
                '<span style="font-weight:600;color:#4caf50;">{}</span>'
                '</span>',
                obj.currency_to.logo.url,
                obj.currency_to.currency
            )
        return obj.currency_to.currency
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
            "1": "#2196f3",  # В обработке
            "2": "#ff9800",  # Ожидание
            "3": "#4caf50",  # Успешно
            "4": "#f44336",  # Ошибка
        }
        return format_html(
            '<span style="display:inline-block; padding:4px 10px; '
            'font-size:12px; font-weight:500; color:white; '
            'background-color:{}; border-radius:4px; '
            'box-shadow:0 1px 2px rgba(0,0,0,0.15);">'
            '{}</span>',
            colors.get(obj.status, "gray"),
            obj.get_status_display()
        )
    colored_status.short_description = "Статус"