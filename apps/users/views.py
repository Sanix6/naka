#restframework
from rest_framework import generics, status, views,permissions
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
import requests
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator



#apps
from .models import User, Verification
from . import serializers
from assets.services.utils import Util, get_password_reset_url
from assets.tamplates import EMAIL_TEMPLATE, NEWPASSWORD_TEMPLATE
from django.conf import settings
from assets.services.sms import send_sms
from assets.services.qrcode import generate_2fa_secret
from assets.services.validators import format_errors
import pyotp

class RegisterView(generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        
        if serializer.is_valid():
            user = serializer.save()

            email_body = EMAIL_TEMPLATE.format(first_name=user.first_name, code=user.code)

            email_data = {
                'email_subject': 'Подтверждение регистрации',
                'email_body': email_body,
                'to_email': user.email
            }
            Util.send_email(email_data)

            return Response({
                "response": True,
                "message": "Пользователь зарегистрирован. Код подтверждения отправлен на вашу электронную почту."
            }, status=status.HTTP_201_CREATED)

        error_message = format_errors(serializer.errors)
        return Response({"response": False, "error": error_message}, status=status.HTTP_400_BAD_REQUEST)



class LoginView(generics.GenericAPIView):
    serializer_class = serializers.LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            totp_code = serializer.validated_data.get('totp_code')

            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return Response({"response": False, "message": "Пользователь не найден."}, status=status.HTTP_400_BAD_REQUEST)

            if not user.check_password(password):
                return Response({"response": False, "message": "Неверный пароль."}, status=status.HTTP_400_BAD_REQUEST)

            if user.is_2fa_enabled:
                if not totp_code:
                    return Response({"response": False, "message": "Необходим код из Google Authenticator."}, status=status.HTTP_401_UNAUTHORIZED)

                totp = pyotp.TOTP(user.totp_secret)
                if not totp.verify(totp_code):
                    return Response({"response": False, "message": "Неверный 2FA код."}, status=status.HTTP_401_UNAUTHORIZED)

            token, _ = Token.objects.get_or_create(user=user)

            return Response({
                "response": True,
                "message": "Успешный вход.",
                "token": token.key
            }, status=status.HTTP_200_OK)
        error_message = format_errors(serializer.errors)
        return Response({
            "response": False,
            "message": "Ошибка при входе.",
            "errors": error_message,
        }, status=status.HTTP_400_BAD_REQUEST)


class ResendConfirmationCodeView(generics.GenericAPIView):
    serializer_class = serializers.ResendEmailSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({
            "response": True,
            "message": "Код подтверждения отправлен повторно."
        }, status=status.HTTP_200_OK)


class TwoFASetupView(views.APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        secret, qr_code = generate_2fa_secret(user)
        user.totp_secret = secret
        user.save()

        return Response({
            "secret": secret,
            "qr_code": qr_code
        })

class TwoFAVerifyView(generics.GenericAPIView):
    serializer_class = serializers.TwoFAVerifySerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        code = serializer.validated_data["code"]

        user = request.user

        if not user.totp_secret:
            return Response({"error": "2FA не инициализирована"}, status=400)

        totp = pyotp.TOTP(user.totp_secret)
        if totp.verify(code):
            user.is_2fa_enabled = True
            user.save()
            return Response({"success": True})

        return Response({"error": "Неверный код"}, status=400)


class TwoFADisableView(views.APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        user.is_2fa_enabled = False
        user.totp_secret = None
        user.save()
        return Response({"response": True, 'message': "2FA успешно отключена."}, status=status.HTTP_200_OK)


class ForgotPasswordView(generics.GenericAPIView):
    serializer_class = serializers.ForgotPasswordSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            user = User.objects.filter(email=email).first()
            if user:
                reset_url = get_password_reset_url(user)
                email_body = NEWPASSWORD_TEMPLATE.format(
                    first_name=user.first_name,
                    reset_url=reset_url
                )
                email_data = {
                    'email_subject': 'Сброс пароля',
                    'email_body': email_body,
                    'to_email': user.email
                }
                Util.send_email(email_data)

                return Response({"response": True, "message": "Ссылка сброса пароля отправлена на вашу почту."}, status=status.HTTP_200_OK)

            return Response({"response": False, "message": "Пользователь с таким email не найден."}, status=status.HTTP_404_NOT_FOUND)

        return Response({"response": False, "message": "Ошибка при сбросе пароля.", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)



class ConfirmCodeView(generics.GenericAPIView):
    serializer_class = serializers.ConfirmCodeSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            code = serializer.validated_data['code']

            try:
                user = User.objects.get(email=email, code=code)
            except User.DoesNotExist:
                return Response({"response": False, "message": "Неверный код подтверждения."}, status=status.HTTP_400_BAD_REQUEST)

            user.is_active = True
            user.save()

            token, _ = Token.objects.get_or_create(user=user)

            return Response({
                "response": True,
                "message": "Аккаунт активирован.",
                "token": token.key
            }, status=status.HTTP_200_OK)

        return Response({
            "response": False,
            "message": "Ошибка при подтверждении кода.",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    


class SetNewPasswordView(generics.GenericAPIView):
    serializer_class = serializers.PasswordResetConfirmSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)


        uidb64 = serializer.validated_data['uidb64']
        token = serializer.validated_data['token']
        password = serializer.validated_data['new_password']

        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return Response({"detail": "Неверная ссылка сброса пароля."}, status=status.HTTP_400_BAD_REQUEST)

        if not default_token_generator.check_token(user, token):
            return Response({"detail": "Неверный или просроченный токен."}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(password)
        user.save()

        return Response({"detail": "Пароль успешно обновлён."}, status=status.HTTP_200_OK)


class LogoutView(views.APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            request.user.auth_token.delete()
        except Token.DoesNotExist:
            pass  
        return Response({"detail": "Вы успешно вышли из системы."}, status=status.HTTP_200_OK)

class DeleteAccountView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        user.delete()
        return Response({"detail": "Аккаунт успешно удалён."}, status=status.HTTP_204_NO_CONTENT)

class PersonalView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.PersonalSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def get(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(user)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class RequestPhoneCodeView(generics.GenericAPIView):
    serializer_class = serializers.RequestPhoneCodeSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        phone = serializer.validated_data['phone']
        user = request.user
        user.code = None  
        user.save()

        message = "Код подтверждения:"
        sms_sent = send_sms(phone, message, user.code)

        if sms_sent:
            return Response({"message": "Код отправлен на номер телефона"})
        return Response({"error": "Ошибка при отправке SMS"}, status=500)

class ConfirmPhoneCodeView(generics.GenericAPIView):
    serializer_class = serializers.ConfirmPhoneCodeSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({
            "response": True,
            "message": "Телефон подтверждён"
        }, status=status.HTTP_200_OK)

class AmlbotKycRequestView(generics.GenericAPIView):
    serializer_class = serializers.AmlbotKycRequestSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        external_applicant_id = str(user.uuid)

        data = {
            "external_applicant_id": external_applicant_id,
            "redirect_url": request.data.get("redirect_url")
        }
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)

        api_token = settings.AMLBOT_API_TOKEN
        url = f'{settings.AML_BASE_URL}/forms/{settings.AML_FORM_ID}/urls'
        headers = {
            'Authorization': f'Token {api_token}'
        }

        try:
            response = requests.post(url, headers=headers, json=serializer.validated_data)
            response_data = response.json()

            if response.status_code == 200:
                verification_id = response_data.get("id") or response_data.get("verification_id")

                if verification_id:
                    Verification.objects.update_or_create(
                        user=user,
                        type="personal",  
                        defaults={
                            "verification_id": verification_id,
                            "is_verified": False
                        }
                    )

            return Response(response_data, status=response.status_code)

        except requests.exceptions.RequestException as e:
            return Response({'error': str(e)}, status=status.HTTP_502_BAD_GATEWAY)

class ProfileNewPasswordView(generics.GenericAPIView):
    serializer_class = serializers.ProfileSetPasswordSerailizer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = request.user
        old_password = serializer.validated_data['old_password']
        password = serializer.validated_data['password']
        confirm_password = serializer.validated_data['confirm_password']

        if not user.check_password(old_password):
            return Response({"error": "Неверный старый пароль."}, status=status.HTTP_400_BAD_REQUEST)
        if password != confirm_password:
            return Response({"error": "Пароли не совпадают."}, status=status.HTTP_400_BAD_REQUEST)
        user.set_password(password)
        user.save()
        return Response({"message": "Пароль успешно изменён."}, status=status.HTTP_200_OK)

        

class LegalVerificationView(generics.GenericAPIView):
    serializer_class = serializers.VerificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)