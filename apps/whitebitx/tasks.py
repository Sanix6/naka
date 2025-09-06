import os
import json
from decimal import Decimal, InvalidOperation, getcontext
from datetime import datetime

import requests
from celery import shared_task, chain
from django.conf import settings
from django.db import transaction
from django.utils import timezone
import uuid
import time

from .models import Rates, HistoryTransactions
from connectors.public.client import WhiteBitClient, WhiteBitPrivateClient
from connectors.private.client import WhiteBitTradeClient

WHITEBIT_BASE_URL = getattr(settings, "WHITEBIT_BASE_URL")
TICKER_URL = f"{WHITEBIT_BASE_URL}/api/v4/public/ticker"
getcontext().prec = 28

WHITEBIT_PUBLIC_KEY = os.getenv("public_key")
WHITEBIT_SECRET_KEY = os.getenv("secret_key")

LOG_DIR = os.path.join(settings.BASE_DIR, "logs")
os.makedirs(LOG_DIR, exist_ok=True)


def write_log(filename: str, message: str):
    filepath = os.path.join(LOG_DIR, filename)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(filepath, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {message}\n")


def _to_decimal(s: str) -> Decimal | None:
    try:
        return Decimal(str(s))
    except (InvalidOperation, TypeError, ValueError):
        return None

    
# === Обновление курсов ===
@shared_task(bind=True, max_retries=3, default_retry_delay=10, rate_limit="10/s", acks_late=True)
def update_rates_from_ticker(self):
    write_log("rates_update.log", "Task started: update_rates_from_ticker")
    try:
        resp = requests.get(TICKER_URL, timeout=8)
        resp.raise_for_status()
        data = resp.json()
        write_log("rates_update.log",
                  f"Fetched {len(data)} pairs from Whitebit API")
    except Exception as e:
        write_log("rates_update.log", f"Error fetching ticker: {e}")
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
        write_log("rates_update.log", f"Updated {len(to_update)} rates")
    else:
        write_log("rates_update.log", "No rates updated")

    if not_found:
        write_log("rates_update.log",
                  f"Missing pairs (first 20): {not_found[:20]}")

    write_log("rates_update.log", "Task finished\n")
    return {"updated": len(to_update), "missing": not_found[:20]}


@shared_task
def close_expired_transactions():
    now = timezone.now()
    updated = HistoryTransactions.objects.filter(
        expired__lt=now
    ).exclude(status="4").update(status="4")
    write_log("transactions.log", f"Closed {updated} expired transactions")
    return f"Обновлено {updated} транзакций"


@shared_task
def check_transactions():
    client = WhiteBitPrivateClient(
        public_key=WHITEBIT_PUBLIC_KEY,
        secret_key=WHITEBIT_SECRET_KEY,
    )

    history_data = client.get_history(transactionMethod=1)
    records = history_data.get("records", [])

    for record in records:
        record_address = record.get("address")
        record_status = record.get("status")
        record_amount = Decimal(record.get("amount", "0"))
        record_txid = record.get("transactionId")

        transactions = HistoryTransactions.objects.filter(
            invoice_from=record_address,
        ).exclude(status="3")

        for tx in transactions:
            if record_status == 3 and record_amount >= tx.amount_from:
                old_status = tx.status
                tx.status = "3"
                tx.transaction_hash = record_txid or ""
                tx.save(update_fields=["status", "transaction_hash"])

                write_log(
                    "check_transactions.log",
                    f"✅ Updated tx {tx.id} | from={record_address} | "
                    f"{old_status} -> 3 | amount_tx={record_amount} | "
                    f"amount_expected={tx.amount_from} | hash={tx.transaction_hash}",
                )
                


@shared_task(bind=True, max_retries=10, default_retry_delay=30)
def transfer_task(self, application_id: int, method: str = "deposit"):
    try:
        tx = HistoryTransactions.objects.select_related("user", "currency_from").get(application_id=application_id)

        if tx.status != "3":
            return application_id 

        user_id = tx.user.id
        ticker = tx.currency_from.currency.upper()
        amount = str(tx.amount_from)

        client = WhiteBitTradeClient(public_key=WHITEBIT_PUBLIC_KEY, secret_key=WHITEBIT_SECRET_KEY)
        result = client.create_transfer(ticker, amount, method)
        
        if "Ошибка 201" in result:
            return application_id

        if "error" in result or "errors" in result:
            write_log("transfer.log", f"ERROR User={user_id}, App={application_id}, {amount} {ticker}, {result}")
            raise self.retry(exc=Exception("Transfer error"))

        tx.inspection = 1
        tx.save(update_fields=["inspection"])
        write_log("transfer.log", f"SUCCESS User={user_id}, App={application_id}, {amount} {ticker}")
        
        market_order_task.apply_async(args=[application_id], countdown=3)

    except HistoryTransactions.DoesNotExist:
        write_log("transfer.log", f"ERROR Application={application_id} not found")
    return application_id


@shared_task(bind=True, max_retries=5, default_retry_delay=20)
def market_order_task(self, application_id: int):
    try:
        tx = HistoryTransactions.objects.select_related("user", "currency_from", "currency_to").get(application_id=application_id)

        if tx.inspection != 1:
            return application_id

        user_id = tx.user.id
        market = f"{tx.currency_to.currency.upper()}_{tx.currency_from.currency.upper()}"
        side = "buy"
        amount = float(tx.total_amount)

        client = WhiteBitTradeClient(public_key=WHITEBIT_PUBLIC_KEY, secret_key=WHITEBIT_SECRET_KEY)
        result = client.create_market_order(market, side, amount)

        if "error" in result:
            write_log("market.log", f"ERROR User={user_id}, App={application_id}, Market={market}, {result}")
            raise self.retry(exc=Exception("Market order error"))

        tx.inspection = 2
        tx.save(update_fields=["inspection"])
        write_log("market.log", f"SUCCESS User={user_id}, App={application_id}, Market={market}, Amount={amount}, {result}")

        transfer_to_main_task.apply_async(args=[application_id], countdown=3)

    except HistoryTransactions.DoesNotExist:
        write_log("market.log", f"ERROR Application={application_id} not found")
    return application_id


@shared_task(bind=True, max_retries=10, default_retry_delay=30)
def transfer_to_main_task(self, application_id: int):
    try:
        tx = HistoryTransactions.objects.select_related("user", "currency_to").get(application_id=application_id)

        if tx.inspection != 2:
            return application_id

        user_id = tx.user.id
        ticker = tx.currency_to.currency.upper()
        amount = str(tx.total_amount)

        client = WhiteBitTradeClient(public_key=WHITEBIT_PUBLIC_KEY, secret_key=WHITEBIT_SECRET_KEY)
        result = client.transfer_to_main(ticker, amount)

        if "error" in result or "errors" in result:
            write_log("trade.log", f"ERROR User={user_id}, App={application_id}, {amount} {ticker}, {result}")
            raise self.retry(exc=Exception("Transfer to main error"))

        tx.inspection = 3
        tx.save(update_fields=["inspection"])
        write_log("trade.log", f"SUCCESS User={user_id}, App={application_id}, {amount} {ticker}")

        withdraw_task.apply_async(args=[application_id], countdown=3)

    except HistoryTransactions.DoesNotExist:
        write_log("trade.log", f"ERROR Application={application_id} not found")
    return application_id


@shared_task(bind=True, max_retries=5, default_retry_delay=10)
def withdraw_task(self, application_id: int):
    try:
        tx = HistoryTransactions.objects.select_related("user", "currency_to").get(application_id=application_id)

        if tx.inspection != 3:
            return application_id

        user_id = tx.user.id
        ticker = tx.currency_to.currency.upper()
        amount = str(tx.total_amount)
        address = tx.invoice_to

        client = WhiteBitTradeClient(public_key=WHITEBIT_PUBLIC_KEY, secret_key=WHITEBIT_SECRET_KEY)
        result = client.withdraw(ticker, amount, address, network="", uniqueId=str(uuid.uuid4()), memo="")

        if "error" in result:
            write_log("withdraw.log", f"ERROR User={user_id}, App={application_id}, {amount} {ticker}, {result}")
            raise self.retry(exc=Exception("Withdraw error"))

        tx.status = "5"  
        tx.transaction_hash = result.get("transactionId", "")
        tx.save(update_fields=["status", "inspection", "transaction_hash"])

        write_log("withdraw.log", f"SUCCESS User={user_id}, App={application_id}, {amount} {ticker}, Address={address}")

    except HistoryTransactions.DoesNotExist:
        write_log("withdraw.log", f"ERROR Application={application_id} not found")
    return application_id



def run_full_trade(application_id: int):
    transfer_task.apply_async(args=[application_id], countdown=3)