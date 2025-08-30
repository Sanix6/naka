from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Verification
from .task import check_verification_status
from datetime import datetime

LOG_FILE = "/home/nako/Nako/logs/kyc.log"


def write_log(message: str):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a") as f:
        f.write(f"[{timestamp}] {message}\n")


@receiver(post_save, sender=Verification)
def start_verification_check(sender, instance, created, **kwargs):
    if instance.verification_id:
        check_verification_status.delay(instance.verification_id)