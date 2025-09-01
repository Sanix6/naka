import random
from django.utils import timezone
from datetime import timedelta

def generate_application_id():
    while True:
        app_id = random.randint(10**7, 10**8 - 1) 
        from apps.whitebitx.models import HistoryTransactions

        if not HistoryTransactions.objects.filter(application_id=app_id).exists():
            return app_id

def get_expired_time():
    timezone.now() + timedelta(minutes=60)