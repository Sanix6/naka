from django.core.mail import EmailMultiAlternatives
import threading
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.urls import reverse
import os
from django.conf import settings
from .token import custom_token_generator
from django.contrib.auth.tokens import default_token_generator




NIKITA_LOGIN = os.getenv("NIKITA_LOGIN")
NIKITA_PASSWORD = os.getenv("NIKITA_PASSWORD")
NIKITA_SENDER = os.getenv("NIKITA_SENDER")


def get_password_reset_url(user):
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = custom_token_generator.make_token(user)
    return f"{settings.FRONTEND_PASSWORD_RESET_URL}?uid={uid}&token={token}"


class EmailThread(threading.Thread):
    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send()

class Util:
    @staticmethod
    def send_email(data):
        email = EmailMultiAlternatives(
            subject=data['email_subject'],
            body=data['email_body'],
            # from_email="support@yourdomain.com",
            to=[data['to_email']]
        )
        email.attach_alternative(data['email_body'], "text/html")
        EmailThread(email).start()



