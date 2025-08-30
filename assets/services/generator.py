import random
from apps.whitebitx.models import HistoryTransactions



def generate_application_id():
    while True:
        app_id = random.randint(10**7, 10**8 - 1) 
        if not HistoryTransactions.objects.filter(application_id=app_id).exists():
            return app_id
