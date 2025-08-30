from rest_framework import serializers
from .models import Finance, Rates, HistoryTransactions

class NetworkSerializer(serializers.ModelSerializer):
    code = serializers.CharField(source="network")
    name = serializers.SerializerMethodField()

    class Meta:
        model = Finance
        fields = ["code", "name", "buy_fee", "sell_fee", "status_buy", "status_sell"]

    def get_name(self, obj):
        return f"{obj.network}" if obj.network else obj.name



class CurrencySerializer(serializers.ModelSerializer):
    code = serializers.CharField(source="currency")
    name = serializers.CharField()
    icon = serializers.SerializerMethodField()
    networks = serializers.SerializerMethodField()

    class Meta:
        model = Finance
        fields = ["id","code", "name", "icon", "networks"]

    def get_icon(self, obj):
        request = self.context.get("request")
        if obj.logo:
            return request.build_absolute_uri(obj.logo.url) if request else obj.logo.url
        return None


    def get_networks(self, obj):
        networks_by_code = self.context.get("networks_by_code", {})
        items = networks_by_code.get(obj.currency, [])
        return NetworkSerializer(items, many=True, context=self.context).data


class RatesSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    base_currency = CurrencySerializer(source="currency_f")
    target_currency = CurrencySerializer(source="currency_t")  
    min_amount = serializers.DecimalField(source="currency_f.min_amount", max_digits=20, decimal_places=8)
    max_amount = serializers.DecimalField(source="currency_f.max_amount", max_digits=20, decimal_places=8)

    class Meta:
        model = Rates
        fields = [
            "id",
            "base_currency",
            "target_currency",  
            "rate",
            "min_amount",
            "max_amount",
            "fixed",
            "updated_at"
        ]

    def get_id(self, obj):
        return f"{obj.currency_f.currency}_{obj.currency_t.currency}"


class CryptoDepositAddressSerializer(serializers.Serializer):
    ticker = serializers.CharField(required=True)
    network = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    # receive_amount = serializers.DecimalField(max_digits=20, decimal_places=8, required=True)
    # send_ticker = serializers.CharField(required=True) 
    # send_network = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    # send_amount = serializers.DecimalField(max_digits=20, decimal_places=8, required=True)
    send_address = serializers.CharField(required=True)


class HistorySerializers(serializers.Serializer):
    transactionMethod = serializers.IntegerField() 
    ticker = serializers.CharField(required=True)
    address = serializers.CharField(required=False, allow_blank=True)
    memo = serializers.CharField(required=False, allow_blank=True)
    addresses = serializers.ListField(child=serializers.CharField(), required=False)
    uniqueId = serializers.CharField(required=False, allow_blank=True)
    limit = serializers.IntegerField(required=False, default=100)
    offset = serializers.IntegerField(required=False, default=0)
    status = serializers.ListField(child=serializers.IntegerField(), required=False)


class HistoryTransactionsSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    currency_from = serializers.SlugRelatedField(
        queryset=Finance.objects.all(),
        slug_field='network'
    )
    currency_to = serializers.SlugRelatedField(
        queryset=Finance.objects.all(),
        slug_field='network'
    )

    class Meta:
        model = HistoryTransactions
        fields = [
            "id",
            "user",
            "currency_from",
            "currency_to",
            "application_id",
            "amount_from",
            "amount_to",
            "rate",
            "fee",
            "created_at",
        ]
