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
        fields = ["id","code", "name", "icon",'decimal', "networks"]

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
    application_id = serializers.IntegerField(required=True)
    invoice_to = serializers.CharField(required=True)


class HistoryTransactionSerializer(serializers.ModelSerializer):
    currency_from = serializers.SlugRelatedField(
        queryset=Finance.objects.all(),
        slug_field='name'
    )
    currency_to = serializers.SlugRelatedField(
        queryset=Finance.objects.all(),
        slug_field='name'
    )
    currency_from_logo = serializers.SerializerMethodField()
    currency_to_logo = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M", read_only=True)

    class Meta:
        model = HistoryTransactions
        fields = [
            "currency_from",
            "currency_to",
            "currency_from_logo",
            "currency_to_logo",
            "application_id",
            "amount_from",
            "amount_to",
            "rate",
            "fee",
            "created_at",
            "type_of_change",
            "invoice_to",
            "invoice_from",
            "status",
            "expired"
        ]

    def get_currency_from_logo(self, obj):
        if obj.currency_from and obj.currency_from.logo:
            return obj.currency_from.logo.url 
        return None

    def get_currency_to_logo(self, obj):
        if obj.currency_to and obj.currency_to.logo:
            return obj.currency_to.logo.url
        return None



class TransactionHistorySerializers(serializers.Serializer):
    transactionMethod = serializers.IntegerField(required=False) 
    address = serializers.CharField(required=False, allow_blank=True)
    uniqueId = serializers.CharField(required=False, allow_blank=True)
    # status = serializers.ListField(child=serializers.IntegerField(), required=False)


class CreateApplicationSerializer(serializers.ModelSerializer):
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
            "type_of_change",
            "currency_from",
            "currency_to",
            "application_id",
            "amount_from",
            "amount_to",
            "rate",
            "fee",
            "created_at",
        ]

    def create(self, validated_data):
        validated_data['status'] = "1"
        return super().create(validated_data)


class StatusSerializers(serializers.Serializer):
    status = serializers.CharField()