from rest_framework import serializers
#django
from django.contrib.auth.password_validation import validate_password
from django.core.mail import send_mail
from assets.services.utils import Util, get_password_reset_url
from assets.tamplates import EMAIL_TEMPLATE
#apps
from .models import User, Verification


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, min_length=8, error_messages={"min_length": "Не менее 8 символов."})
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
    totp_code = serializers.CharField(required=False, allow_blank=True)

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


class ResendEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True, error_messages={"required": "Email обязателен."})

    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Пользователь с таким email не найден.")
        return value

    def save(self, **kwargs):
        email = self.validated_data['email']
        user = User.objects.get(email=email)

        email_body = EMAIL_TEMPLATE.format(first_name=user.first_name, code=user.code)

        email_data = {
            'email_subject': 'Код подтверждения регистрации',
            'email_body': email_body,
            'to_email': user.email
        }

        Util.send_email(email_data)

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
    
class ConfirmPhoneCodeSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=15)
    code = serializers.CharField(max_length=6)

    def validate(self, attrs):
        phone = attrs.get("phone")
        code = attrs.get("code")

        if not User.objects.filter(phone=phone, code=code).exists():
            raise serializers.ValidationError({"code": "Неверный код подтверждения."})
        return attrs

    def save(self, **kwargs):
        phone = self.validated_data['phone']
        code = self.validated_data['code']
        user = User.objects.get(phone=phone)
        
        if str(user.code) != str(code):
            raise serializers.ValidationError({"code": "Неверный код подтверждения."})

        user.phone_verified = True
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


class RequestPhoneCodeSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=15)



class SetProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'phone', 'avatar')

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.avatar = validated_data.get('avatar', instance.avatar)
        instance.save()
        return instance


class PersonalSerializer(serializers.ModelSerializer):
    last_activity = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ('uuid', 'phone', 'first_name', 'last_name', 'surname', 'birth_date', 'country', 'last_activity', 'is_2fa_enabled', 'email',)
    
    def get_last_activity(self, obj):
        if obj.last_activity:
            return obj.last_activity.strftime('%Y-%m-%d %H:%M')
        return None
    
class AmlbotKycRequestSerializer(serializers.Serializer):
    redirect_url = serializers.URLField()


class TwoFAVerifySerializer(serializers.Serializer):
    code = serializers.CharField(required=True, help_text="Код из приложения 2FA")



class PasswordResetConfirmSerializer(serializers.Serializer):
    uidb64 = serializers.CharField(required=True, help_text="UID пользователя")
    token = serializers.CharField(required=True, help_text="Токен для сброса пароля")
    new_password = serializers.CharField(write_only=True, min_length=8)
    confirm_password = serializers.CharField(write_only=True, min_length=8)

    def validate(self, attrs):
        new_password = attrs.get("new_password")
        confirm_password = attrs.get("confirm_password")

        if new_password != confirm_password:
            raise serializers.ValidationError({"non_field_errors": ["Пароли не совпадают!"]})

        validate_password(new_password)

        return attrs


class ProfileSetPasswordSerailizer(serializers.Serializer):
    old_password = serializers.CharField(required=True, write_only=True)
    password = serializers.CharField(required=True, write_only=True, min_length=8, error_messages={"min_length": "Не менее 8 символов."})
    confirm_password = serializers.CharField(required=True, write_only=True, min_length=8, error_messages={"min_length": "Не менее 8 символов."})

    def validate(self, attrs):
        old_password = attrs.get("old_password")
        password = attrs.get("password")
        confirm_password = attrs.get("confirm_password")

        if password != confirm_password:
            raise serializers.ValidationError({"non_field_errors": ["Пароли не совпадают!"]})
        if old_password == password:
            raise serializers.ValidationError({"password": "Новый пароль не должен совпадать со старым паролем."})
        if old_password != old_password:
            raise serializers.ValidationError({"old_password": "Старый пароль неверен."})

        validate_password(password)

        return attrs



class VerificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Verification
        fields = [
            "type", "name", "inn", "address", "country",
            "passport_front", "passport_back", "registration_doc",
            "license_doc", "additional_doc"
        ]