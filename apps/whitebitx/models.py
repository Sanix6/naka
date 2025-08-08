from django.db import models


class Finance(models.Model):
    name = models.CharField(max_length=100) 
    currency = models.CharField(max_length=10) 
    network = models.CharField(max_length=50, blank=True, null=True) 
    logo = models.ImageField(upload_to='finance_logos/', blank=True, null=True)
    decimals = models.PositiveIntegerField(default=2)  
    min_amount = models.DecimalField(max_digits=20, decimal_places=8, default=0.01)
    max_amount = models.DecimalField(max_digits=20, decimal_places=8, default=1000.00)
    sell_fee = models.DecimalField(max_digits=20, decimal_places=8, default=0.00000000)
    buy_fee = models.DecimalField(max_digits=20, decimal_places=8, default=0.00000000)
    explorer_url = models.URLField(blank=True, null=True)  
    status_b = models.BooleanField(default=True)  
    status_s = models.BooleanField(default=True)  

    def __str__(self):
        return f"{self.currency} ({self.network or 'Mainnet'})"

    class Meta:
        verbose_name = 'Finance'
        verbose_name_plural = 'Finances'
        ordering = ['currency', 'network']


class Rate(models.Model):
    base_currency = models.ForeignKey(
        Finance, on_delete=models.CASCADE, related_name='rates_from'
    )
    quote_currency = models.ForeignKey(
        Finance, on_delete=models.CASCADE, related_name='rates_to'
    )
    rate_sell = models.DecimalField(max_digits=55, decimal_places=8, default=1)
    rate_buy = models.DecimalField(max_digits=55, decimal_places=8, default=1)
    is_fixed_rate_available = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.base_currency.currency}_{self.quote_currency.currency}"

    class Meta:
        verbose_name = 'Rate'
        verbose_name_plural = 'Rates'
        ordering = ['base_currency', 'quote_currency']