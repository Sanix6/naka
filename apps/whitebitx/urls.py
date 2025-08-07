from django.urls import path, include
from .views import *

urlpatterns = [
    path('markets/', MarketsView.as_view(), name='markets'),
]