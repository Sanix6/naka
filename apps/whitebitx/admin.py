from django.contrib import admin
from .models import Finance, Rates, HistoryTransactions
from unfold.admin import ModelAdmin
from django.utils.html import mark_safe

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
    list_display = ('get_currency_from',  'get_currency_to','rate', 'fixed', 'updated_at')
    search_fields = ('currency_f__currency', 'currency_t__currency')

    def get_currency_from(self, obj):
        return obj.currency_f.currency
    get_currency_from.short_description = 'From'

    def get_currency_to(self, obj):
        return obj.currency_t.currency
    get_currency_to.short_description = 'To'




@admin.register(HistoryTransactions)
class HistoryTransactionsAdmin(admin.ModelAdmin):
    list_display = (
        "user", "currency_from", "amount_from",
        "currency_to", "amount_to", "rate", "fee",'colored_status', "created_at", "type_of_change"
    )
    search_fields = ("user__username", "currency_from__currency", "currency_to__currency")
    list_filter = ('user', 'currency_from', 'currency_to',  'status', "created_at", "type_of_change")
    date_hierarchy = "created_at"
    ordering = ("-created_at",)

    def colored_status(self, obj):
        colors = {
            "1": "#2196f3",
            "2": "#ff9800",
            "3": "#4caf50",
            "4": "#f44336",
        }
        icons = {
            "1": "🆕",
            "2": "⏳",
            "3": "✅",
            "4": "❌",
        }
        return format_html(
            '<span style="background-color:{}; color:white; padding:3px 8px; border-radius:6px;">{} {}</span>',
            colors.get(obj.status, "gray"),
            icons.get(obj.status, "❔"),
            obj.get_status_display()
        )