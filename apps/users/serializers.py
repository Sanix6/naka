from rest_framework import serializers
#django
from django.contrib.auth.password_validation import validate_password
from django.core.mail import send_mail

#apps
from .models import User


class RegisterSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True, required=True, min_length=8,error_messages={"min_length": "Не менее 8 символов."})

    class Meta:
        model = User
        fields = ('email', 'password', 'confirm_password')

    def validate(self, attrs):
        password = attrs.get("password")
        confirm_password = attrs.get("confirm_password")
        validate_password(password)

        if password != confirm_password:
            raise serializers.ValidationError({"password": "Пароли не совпадают!"})
        return attrs

    def create(self, validated_data):
        validated_data.pop("confirm_password")
        user = User(**validated_data)
        user.set_password(validated_data["password"])
        user.save()

        # send_mail(
        #     "Подтверждение email",
        #     f"Ваш код подтверждения: {user.code}",
        #     "smtp.yandex.ru",
        #     [user.email],
        #     fail_silently=False,
        # )

        return user
    

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True, error_messages={"required": "Email обязателен."})
    password = serializers.CharField(required=True, write_only=True, error_messages={"required": "Пароль обязателен."})

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError({"email": "Пользователь с таким email не найден."})

        user = User.objects.get(email=email)
        if not user.check_password(password):
            raise serializers.ValidationError({"password": "Неверный пароль."})
        return attrs
    

class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True, error_messages={"required": "Email обязателен."})

    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Пользователь с таким email не найден.")
        return value

    def save(self, **kwargs):
        email = self.validated_data['email']
        user = User.objects.get(email=email)
        user.save()  
        return user
    

class ConfirmCodeSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True, error_messages={"required": "Email обязателен."})
    code = serializers.IntegerField(required=True, error_messages={"required": "Код обязателен."})

    def validate(self, attrs):
        email = attrs.get("email")
        code = attrs.get("code")

        if not User.objects.filter(email=email, code=code).exists():
            raise serializers.ValidationError({"code": "Неверный код активации."})
        return attrs

    def save(self, **kwargs):
        email = self.validated_data['email']
        user = User.objects.get(email=email)
        user.is_active = True
        user.save()
        return user
    
    
class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(
        required=True,
        write_only=True,
        min_length=8,
        error_messages={"min_length": "Не менее 8 символов."}
    )
    confirm_password = serializers.CharField(
        required=True,
        write_only=True,
        min_length=8,
        error_messages={"min_length": "Не менее 8 символов."}
    )

    def validate(self, attrs):
        password = attrs.get("password")
        confirm_password = attrs.get("confirm_password")

        if password != confirm_password:
            raise serializers.ValidationError({"non_field_errors": ["Пароли не совпадают!"]})

        validate_password(password)

        return attrs