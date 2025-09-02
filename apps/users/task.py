import requests
from datetime import datetime
from celery import shared_task
from .models import Verification

LOG_FILE = "/home/nako/Nako/logs/kyc.log"


def write_log(message: str):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a") as f:
        f.write(f"[{timestamp}] {message}\n")

@shared_task(bind=True, max_retries=None)
def check_verification_status(self, verification_id: str):
    url = f"https://kyc-api.amlbot.com/verifications/{verification_id}"
    from django.conf import settings
    headers = {"Authorization": f"Token {settings.AMLBOT_API_TOKEN}"}

    write_log(f"▶️ Start check: verification_id={verification_id}")

    try:
        resp = requests.get(url, headers=headers, timeout=10)
        data = resp.json()
    except Exception as e:
        write_log(f"❌ Request error: verification_id={verification_id}, error={e}")
        raise self.retry(exc=e, countdown=5)

    status = data.get("status")
    verified = data.get("verified")
    write_log(f"📩 Response: verification_id={verification_id}, status={status}, verified={verified}")

    if status == "completed":
        v = Verification.objects.filter(verification_id=verification_id).first()
        if v:
            v.is_verified = verified
            v.save(update_fields=["is_verified"])

            user_info = f"user_id={v.user_id}, username={v.user.username}"
            if verified:
                write_log(f"✅ Verification SUCCESS: {user_info}, verification_id={verification_id}")
            else:
                write_log(f"⚠️ Verification FAILED: {user_info}, verification_id={verification_id}")

        if verified is not None:
            return f"Verification {verification_id} completed, verified={verified}"

    self.retry(countdown=5)
