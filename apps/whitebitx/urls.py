from django.urls import path, include
from .views import *

urlpatterns = [
    path('markets/', MarketsView.as_view(), name='markets'),
    path('ticker/', TickerView.as_view(), name='ticker'),
    path('fee/', FeeView.as_view(), name='fee'),
    path('currencies/', CurrencyListView.as_view(), name='currencies'),
    path('main-address/', CryptoDepositAddressGenericView.as_view(), name='crypto_deposit_address'),
    path('transaction-history/', TransactionHistoryView.as_view(), name='history_changes'),
    path('main-applications/', CreateApplicationView.as_view(), name='application-history'),
    path('main-balance', GETBalance.as_view()),
    path('main-transaction-list', TransactionsListView.as_view()),
    path('status/', StatusView.as_view())
]