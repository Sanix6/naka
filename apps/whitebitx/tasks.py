from decimal import Decimal, InvalidOperation, getcontext
from django.db import transaction
from django.conf import settings
from celery import shared_task
import requests
import os
from datetime import datetime

from .models import Rates, Finance 

WHITEBIT_BASE_URL = getattr(settings, "WHITEBIT_BASE_URL")
TICKER_URL = f"{WHITEBIT_BASE_URL}/api/v4/public/ticker"
getcontext().prec = 28

LOG_FILE = "/home/nako/Nako/logs/rates_update.log"



def log_message(msg: str):
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{datetime.now().isoformat()}] {msg}\n")


def _to_decimal(s: str) -> Decimal:
    try:
        return Decimal(str(s))
    except (InvalidOperation, TypeError, ValueError):
        return None


@shared_task(bind=True, max_retries=3, default_retry_delay=10, rate_limit="10/s", acks_late=True)
def update_rates_from_ticker(self):
    log_message("Task started: update_rates_from_ticker")
    try:
        resp = requests.get(TICKER_URL, timeout=8)
        resp.raise_for_status()
        data = resp.json()
        log_message(f"Fetched {len(data)} pairs from Whitebit API")
    except Exception as e:
        log_message(f"Error fetching ticker: {e}")
        raise

    prices = {}
    for pair_key, payload in data.items():
        lp = payload.get("last_price")
        d = _to_decimal(lp)
        if d is not None and d > 0:
            prices[pair_key.upper()] = d

    to_update = []
    not_found = []

    qs = Rates.objects.select_related("currency_f", "currency_t").only(
        "id", "rate", "currency_f__currency", "currency_t__currency"
    )

    for r in qs:
        base = r.currency_f.currency.upper()
        quote = r.currency_t.currency.upper()
        direct_key = f"{base}_{quote}"
        inverse_key = f"{quote}_{base}"

        new_rate = None

        if direct_key in prices:
            new_rate = prices[direct_key]
        elif inverse_key in prices:
            try:
                new_rate = Decimal(1) / prices[inverse_key]
            except (InvalidOperation, ZeroDivisionError):
                new_rate = None

        if new_rate is not None:
            r.rate = float(new_rate)
            to_update.append(r)
        else:
            not_found.append(direct_key)

    if to_update:
        with transaction.atomic():
            Rates.objects.bulk_update(to_update, ["rate"])
        log_message(f"Updated {len(to_update)} rates")
    else:
        log_message("No rates updated")

    if not_found:
        log_message(f"Missing pairs (first 20): {not_found[:20]}")

    log_message("Task finished\n")
    return {"updated": len(to_update), "missing": not_found[:20]}
