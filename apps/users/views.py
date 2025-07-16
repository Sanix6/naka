#restframework
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

#apps
from .models import User
from . import serializers
from assets.services.utils import Util
from assets.tamplates import EMAIL_TEMPLATE


class RegisterView(generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            email_body = EMAIL_TEMPLATE.format(first_name=user.first_name, code=user.code)

            email_data = {'email_subject': 'Подтверждение регистрации','email_body': email_body,'to_email': user.email}
            Util.send_email(email_data)

            return Response({"response": True,
                "message": "Пользователь зарегистрирован. Код подтверждения отправлен на вашу электронную почту."
            }, status=status.HTTP_201_CREATED)

        return Response({"response": False,"message": "Ошибка при регистрации пользователя."
        }, status=status.HTTP_400_BAD_REQUEST)


class LoginView(generics.GenericAPIView):
    serializer_class = serializers.LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = User.objects.get(email=serializer.validated_data['email'])
            if user.check_password(serializer.validated_data['password']):
                return Response({"response": True, "message": "Успешный вход."}, status=status.HTTP_200_OK)

            return Response({"response": False, "message": "Неверный пароль."}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"response": False, "message": "Ошибка при входе.", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    


class ForgotPasswordView(generics.GenericAPIView):
    serializer_class = serializers.ForgotPasswordSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            if User.objects.filter(email=email).exists():
                user = User.objects.get(email=email)
                email_body = EMAIL_TEMPLATE.format(first_name=user.first_name, code=user.code)

                email_data = {'email_subject': 'Сброс пароля', 'email_body': email_body, 'to_email': user.email}
                Util.send_email(email_data)

                return Response({"response": True, "message": "Код сброса пароля отправлен на вашу электронную почту."}, status=status.HTTP_200_OK)

            return Response({"response": False, "message": "Пользователь с таким email не найден."}, status=status.HTTP_404_NOT_FOUND)

        return Response({"response": False, "message": "Ошибка при сбросе пароля.", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    

class ConfirmCodeView(generics.GenericAPIView):
    serializer_class = serializers.ConfirmCodeSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            code = serializer.validated_data['code']

            if User.objects.filter(email=email, code=code).exists():
                user = User.objects.get(email=email, code=code)
                user.is_active = True
                user.save()

                return Response({"response": True, "message": "Аккаунт активирован."}, status=status.HTTP_200_OK)

            return Response({"response": False, "message": "Неверный код подтверждения."}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"response": False, "message": "Ошибка при подтверждении кода.", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    

class SetNewPasswordView(generics.GenericAPIView):
    serializer_class = serializers.SetNewPasswordSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = request.user
        user.set_password(serializer.validated_data['password'])
        user.save()

        return Response({"detail": "Пароль успешно обновлён."}, status=status.HTTP_200_OK)