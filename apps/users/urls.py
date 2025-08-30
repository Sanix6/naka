from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

urlpatterns = [
    path('register/', RegisterView.as_view(), name='auth'),
    path('resend-confirmation-email/', ResendConfirmationCodeView.as_view(), name='auth'),
    path('login/', LoginView.as_view(), name='auth'),
    path('2fa/setup/', TwoFASetupView.as_view()),
    path('2fa/verify/', TwoFAVerifyView.as_view()),
    path('2fa/disable/', TwoFADisableView.as_view()),
    path('confirm-code/', ConfirmCodeView.as_view(), name='auth'),
    path('forgot-password/', ForgotPasswordView.as_view(), name='password-reset-confirm'),
    path('set-password/', SetNewPasswordView.as_view(), name='password-reset'),
    path('logout/', LogoutView.as_view(), name='auth'),
    path('delete-account/', DeleteAccountView.as_view(), name='auth'),
    path('personal-info/', PersonalView.as_view(), name='auth'),
    path('profile/request-phone-code/', RequestPhoneCodeView.as_view()),
    path('profile/confirm-phone-code/', ConfirmPhoneCodeView.as_view()),
    path('kyc-verification/', AmlbotKycRequestView.as_view(), name='kyc-verification'),
    path("create-verification/", LegalVerificationView.as_view(), name="verification-create"),
    path('profile/new_password/', ProfileNewPasswordView.as_view(), name='new-password'),
]