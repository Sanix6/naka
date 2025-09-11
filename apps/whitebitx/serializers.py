from rest_framework import serializers
from .models import Finance, Rates, HistoryTransactions
from django.utils import timezone
from decimal import Decimal, ROUND_DOWN


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
        fields = ["id","code", "min_amount", "max_amount", "name", "icon",'decimal', 'fee',"networks"]

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

    class Meta:
        model = Rates
        fields = [
            "id",
            "base_currency",
            "target_currency",  
            "rate",
            "fixed",
            "updated_at"
        ]

    def get_id(self, obj):
        return f"{obj.currency_f.currency}_{obj.currency_t.currency}"


class CryptoDepositAddressSerializer(serializers.Serializer):
    application_id = serializers.IntegerField(required=True)
    invoice_to = serializers.CharField(required=True)

    def create(self, validated_data):
        validated_data['status'] = "2"
        return super().create(validated_data)


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
    expired = serializers.SerializerMethodField()  

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
    
    def get_expired(self, obj):
        if obj.expired:
            local_expired = timezone.localtime(obj.expired)  
            return local_expired.strftime("%H:%M")
        return None

    def create(self, validated_data):
        validated_data['status'] = "2"
        return super().create(validated_data)



class TransactionHistorySerializers(serializers.Serializer):
    transactionMethod = serializers.IntegerField(required=False) 
    address = serializers.CharField(required=False, allow_blank=True)
    uniqueId = serializers.CharField(required=False, allow_blank=True)
    # status = serializers.ListField(child=serializers.IntegerField(), required=False)


class CreateApplicationSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    currency_from = serializers.SlugRelatedField(
        queryset=Finance.objects.all(),
        slug_field='network',
    )
    currency_to = serializers.SlugRelatedField(
        queryset=Finance.objects.all(),
        slug_field='network',
    )

    class Meta:
        model = HistoryTransactions
        fields = [
            "id",
            "user",
            "type_of_change",
            "currency_from",
            "currency_to",
            "amount_from",
            "amount_to",
            "network_from",
            "network_to",
            "application_id",
            "rate",
            "fee",
            "created_at",
        ]

    def create(self, validated_data):
        validated_data['status'] = "1"
        return super().create(validated_data)
    
    def validate(self, data):
        amount_from = data['amount_from']
        currency_from = data['currency_from']
        currency_to = data['currency_to']
        
        try:
            rate = Rates.objects.get(currency_f=currency_from, currency_t=currency_to)
        except Rates.DoesNotExist:
            raise serializers.ValidationError("Курс не найден для выбранных валют.")

        amount_to = amount_from * rate.rate
        
        amount_to -= (amount_to * rate.fixed / 100) 

        finance = Finance.objects.get(network=currency_to.network)
        amount_to -= finance.fee

        data['amount_to'] = amount_to
        return data


class StatusSerializers(serializers.Serializer):
    status = serializers.CharField()


class WithdrawSerializer(serializers.Serializer):
    ticker = serializers.CharField()
    amount = serializers.CharField()
    address = serializers.CharField()
    network = serializers.CharField()
    memo = serializers.CharField(required=False, allow_blank=True)