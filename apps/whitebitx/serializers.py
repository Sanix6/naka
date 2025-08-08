from rest_framework import serializers
from .models import Finance, Rate


class NetworkSerializer(serializers.ModelSerializer):
    code = serializers.CharField(source="network")
    name = serializers.SerializerMethodField()
    min_deposit = serializers.DecimalField(source="min_amount", max_digits=20, decimal_places=8)
    fee = serializers.DecimalField(source="sell_fee", max_digits=20, decimal_places=8)
    explorer_url = serializers.URLField()

    class Meta:
        model = Finance
        fields = ["code", "name", "min_deposit", "fee", "explorer_url"]

    def get_name(self, obj):
        return f"{obj.network} Network" if obj.network else obj.name


class CurrencySerializer(serializers.ModelSerializer):
    code = serializers.CharField(source="currency")
    name = serializers.CharField()
    icon = serializers.SerializerMethodField()
    networks = serializers.SerializerMethodField()

    class Meta:
        model = Finance
        fields = ["code", "name", "icon", "networks"]

    def get_icon(self, obj):
        request = self.context.get("request")
        if obj.logo:
            return request.build_absolute_uri(obj.logo.url) if request else obj.logo.url
        return None

    def get_networks(self, obj):
        return [NetworkSerializer(obj, context=self.context).data]


class RatePairSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    base_currency = CurrencySerializer(source="base_currency")
    quote_currency = CurrencySerializer(source="quote_currency")
    rate = serializers.DecimalField(source="rate_sell", max_digits=55, decimal_places=8)
    min_amount = serializers.DecimalField(source="base_currency.min_amount", max_digits=20, decimal_places=8)
    max_amount = serializers.DecimalField(source="base_currency.max_amount", max_digits=20, decimal_places=8)
    is_fixed_rate_available = serializers.BooleanField()

    class Meta:
        model = Rate
        fields = [
            "id",
            "base_currency",
            "quote_currency",
            "rate",
            "min_amount",
            "max_amount",
            "is_fixed_rate_available"
        ]

    def get_id(self, obj):
        return f"{obj.base_currency.currency}_{obj.quote_currency.currency}"