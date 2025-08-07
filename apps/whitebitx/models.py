from django.db import models


class Finance(models.Model):
    name = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='finance_logos/', blank=True, null=True)
    currency = models.CharField(max_length=10)
    network = models.CharField(max_length=50, blank=True, null=True)
    decimal = models.IntegerField(default=2)
    min_amount = models.DecimalField(max_digits=20, decimal_places=8, default=0.01)
    max_amount = models.DecimalField(max_digits=20, decimal_places=8, default=1000.00)
    sell_fee = models.DecimalField(max_digits=20, decimal_places=8, default=0.000)
    buy_fee = models.DecimalField(max_digits=20, decimal_places=8, default=0.000)
    status_b = models.BooleanField(default=True)
    status_s = models.BooleanField(default=True)


    def __str__(self):
        return f"{self.name} ({self.currency})"

    class Meta:
        verbose_name = 'Finance'
        verbose_name_plural = 'Finances'
        ordering = ['name']


class Rates(models.Model):
    currency_f = models.ForeignKey(Finance,on_delete=models.CASCADE, related_name='currency_f')
    currency_t = models.ForeignKey(Finance, on_delete=models.CASCADE, related_name='currency_t')
    rate_sell = models.DecimalField(max_digits=55, decimal_places=8, default=1)
    rate_buy = models.DecimalField(max_digits=55, decimal_places=8, default=1)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.currency_f}/{self.currency_t}"

    class Meta:
        verbose_name = 'Rate'
        verbose_name_plural = 'Rates'
        ordering = ['currency_f', 'currency_t']
