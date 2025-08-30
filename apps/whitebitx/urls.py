from django.urls import path, include
from .views import *

urlpatterns = [
    path('markets/', MarketsView.as_view(), name='markets'),
    path('ticker/', TickerView.as_view(), name='ticker'),
    path('fee/', FeeView.as_view(), name='fee'),
    path('currencies/', CurrencyListView.as_view(), name='currencies'),
    path('get-address/', CryptoDepositAddressGenericView.as_view(), name='crypto_deposit_address'),
    path('transaction-history/', CheckStatusView.as_view(), name='history_changes'),
    path('applications-history/', HistoryTransactionsCreateView.as_view(), name='application-history')
]