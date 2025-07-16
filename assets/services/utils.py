from django.core.mail import EmailMultiAlternatives
import threading

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
