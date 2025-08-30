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
        "currency_to", "amount_to", "rate", "fee", "created_at"
    )
    search_fields = ("user__username", "currency_from__currency", "currency_to__currency")
    list_filter = ("currency_from", "currency_to", "created_at")
    date_hierarchy = "created_at"
    ordering = ("-created_at",)