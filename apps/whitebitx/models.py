from django.db import models
from django.conf import settings
from apps.users.models import User
from assets.choices import *
from assets.services.generator import *
from decimal import Decimal,ROUND_DOWN




class Finance(models.Model):
    name = models.CharField(max_length=100) 
    currency = models.CharField(max_length=10, db_index=True)  
    network = models.CharField(max_length=50, unique=True, blank=True, null=True)
    logo = models.ImageField(upload_to='finance_logos/', blank=True, null=True)

    decimal = models.PositiveIntegerField(default=8, help_text="Количество знаков после запятой")
    min_amount = models.DecimalField(max_digits=20, decimal_places=2, default=0.01)
    max_amount = models.DecimalField(max_digits=20, decimal_places=8, default=1000.00)

    sell_fee = models.DecimalField(max_digits=20, decimal_places=8, default=0)
    buy_fee = models.DecimalField(max_digits=20, decimal_places=8, default=0)

    status_buy = models.BooleanField(default=True, help_text="Доступна для покупки")
    status_sell = models.BooleanField(default=True, help_text="Доступна для продажи")

    def __str__(self):
        return f"{self.name} ({self.network or 'Mainnet'})"

    class Meta:
        verbose_name = 'Валюта'
        verbose_name_plural = 'Валюты'
        ordering = ['currency', 'network']


class Rates(models.Model):
    currency_f = models.ForeignKey(Finance, on_delete=models.CASCADE, related_name='rates_from')
    currency_t = models.ForeignKey(Finance, on_delete=models.CASCADE, related_name='rates_to')
    rate = models.DecimalField(max_digits=30, decimal_places=12, default=0)
    fixed  = models.DecimalField(max_digits=30, decimal_places=12, default=0)
    rate_sell = models.DecimalField(max_digits=20, decimal_places=10, default=1)
    rate_buy = models.DecimalField(max_digits=20, decimal_places=10, default=1)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.currency_f.currency}/{self.currency_t.currency}"

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'
        ordering = ['currency_f', 'currency_t']
        constraints = [
            models.UniqueConstraint(fields=['currency_f', 'currency_t'], name='unique_currency_pair')
        ]


class HistoryTransactions(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Пользователь"
    )
    currency_from = models.ForeignKey(
        Finance,
        on_delete=models.CASCADE,
        related_name="history_from",
        verbose_name="Валюта списания (откуда)"
    )
    currency_to = models.ForeignKey(
        Finance,
        on_delete=models.CASCADE,
        related_name="history_to",
        verbose_name="Валюта зачисления (куда)"
    )
    network_from = models.CharField(
        max_length=25,
        null=True, blank=True
    )
    network_to = models.CharField(
        max_length=25,
        null=True, blank=True
    )
    memo = models.CharField(
        max_length=255,
        null=True, blank=True
    )
    application_id = models.IntegerField(
        unique=True,
        verbose_name="ID заявки"
    )
    amount_from = models.DecimalField(
        max_digits=20,
        decimal_places=8,
        verbose_name="Сумма списания"
    )
    amount_to = models.DecimalField(
        max_digits=20,
        decimal_places=8,
        verbose_name="Сумма зачисления"
    )
    total_amount = models.DecimalField(
        max_digits=20,
        decimal_places=8,
        verbose_name="Сумма с учетом коммиссии"
    )
    rate = models.DecimalField(
        max_digits=30,
        decimal_places=12,
        verbose_name="Курс"
    )
    fee = models.DecimalField(
        max_digits=20,
        decimal_places=5,
        default=0,
        verbose_name="Комиссия"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания"
    )
    type_of_change = models.CharField(
        "Тип заявки",
        max_length=25,
        choices=TYPE_OF_CHANGE_CHOICES
    )
    invoice_to = models.CharField(
        "Счет получателя",
        max_length=155,
        null=True, blank=True
    )
    invoice_from = models.CharField(
        "Счет отправителя",
        max_length=155,
        null=True, blank=True
    )
    status = models.CharField(
        "Статус",
        max_length=77,
        choices=STATUS_CHOICES
    )
    inspection = models.IntegerField(
        default=0
    )
    #0 = ничего, 1 = transfer, 2 = trade, 3 = transfer_to_main, 4 = withdraw
    expired = models.DateTimeField(
        verbose_name="Срок действия",
        null=True, blank=True
    )
    transaction_hash = models.CharField(
        max_length=255,
        null=True, blank=True
    )

    class Meta:
        verbose_name = "История транзакции"
        verbose_name_plural = "Истории транзакций"
        
        
    def __str__(self):
        return f"{self.user} {self.amount_from} {self.currency_from.currency} → {self.amount_to} {self.currency_to.currency}"
    
        
    def save(self, *args, **kwargs):
        fee_amount = (self.amount_from * self.fee) / 100
        self.total_amount = self.amount_from - fee_amount
        self.total_amount = self.total_amount * self.rate

        decimal_places_to = self.currency_to.decimal
        self.total_amount = self.total_amount.quantize(Decimal(10) ** -decimal_places_to)

        super().save(*args, **kwargs)
