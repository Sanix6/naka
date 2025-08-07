from django.contrib import admin
from .models import Finance, Rates

@admin.register(Finance)
class FinanceAdmin(admin.ModelAdmin):
    list_display = ('name', 'currency', 'network', 'decimal', 'min_amount', 'max_amount', 'sell_fee', 'buy_fee', 'status_b', 'status_s')
    search_fields = ('name', 'currency')
    list_filter = ('status_b', 'status_s')

@admin.register(Rates)
class RatesAdmin(admin.ModelAdmin):
    list_display = ('currency_f', 'currency_t', 'rate_sell', 'rate_buy', 'updated_at')
    search_fields = ('currency_f', 'currency_t')
