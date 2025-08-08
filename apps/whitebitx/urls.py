from django.urls import path, include
from .views import *

urlpatterns = [
    path('markets/', MarketsView.as_view(), name='markets'),
    path('ticker/', TickerView.as_view(), name='ticker'),
    path('fee/', FeeView.as_view(), name='fee'),
    path('currencies/', CurrencyView.as_view(), name='currencies'),

]