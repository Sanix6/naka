from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import HistoryTransactions
from .tasks import run_full_trade

@receiver(post_save, sender=HistoryTransactions)
def start_trade_pipeline(sender, instance, created, **kwargs):
    if instance.status == "3" and instance.inspection == 0:
        run_full_trade(instance.application_id)
