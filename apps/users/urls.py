from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *


# router = DefaultRouter()
# router.register(r'user', PersonalView, basename='auth')

urlpatterns = [
    path('register/', RegisterView.as_view(), name='auth'),
    path('login/', LoginView.as_view(), name='auth'),
    path('forgot-password/', ForgotPasswordView.as_view(), name='auth'),
    path('confirm-code/', ConfirmCodeView.as_view(), name='auth'),
    # path('', include(router.urls)),
]