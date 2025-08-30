from django.shortcuts import render
from rest_framework import generics, status, views, permissions
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from connectors.public.client import WhiteBitClient, WhiteBitPrivateClient
from collections import defaultdict
from .serializers import *
from assets.services.generator import generate_application_id
import os


class CryptoDepositAddressGenericView(generics.GenericAPIView):
    serializer_class = CryptoDepositAddressSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        ticker = serializer.validated_data['ticker']
        network = serializer.validated_data.get('network', None)
        send_address = serializer.validated_data['send_address']

        public_key = os.getenv('public_key')
        secret_key = os.getenv('secret_key')
        

        
        client = WhiteBitPrivateClient(public_key, secret_key)  
        result = client.get_address(ticker, network)  
        
        if 'error' in result:
            return Response(result, status=status.HTTP_400_BAD_REQUEST)
        return Response(result, status=status.HTTP_200_OK)

class CheckStatusView(generics.GenericAPIView):
    serializer_class = HistorySerializers

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        
        if serializer.is_valid():
            transaction_method = serializer.validated_data['transactionMethod']
            ticker = serializer.validated_data.get('ticker')
            address = serializer.validated_data.get('address')
            memo = serializer.validated_data.get('memo')
            addresses = serializer.validated_data.get('addresses')
            unique_id = serializer.validated_data.get('uniqueId')
            limit = serializer.validated_data.get('limit', 100)
            offset = serializer.validated_data.get('offset', 0)
            status_list = serializer.validated_data.get('status')

            client = WhiteBitPrivateClient(public_key='45f78aa66fb498abdae7c3883fb57ccd', secret_key='c27bb4c14b1e9eaff868548c1ff76d04')

            history_data = client.get_history(
                transactionMethod=transaction_method,
                ticker=ticker,
                address=address,
                memo=memo,
                addresses=addresses,
                uniqueId=unique_id,
                limit=limit,
                offset=offset,
                status=status_list
            )

            if 'error' in history_data:
                return Response(history_data, status=status.HTTP_400_BAD_REQUEST)

            return Response(history_data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class HistoryTransactionsCreateView(generics.GenericAPIView):
    serializer_class = HistoryTransactionsSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        data = request.data.copy()
        data["user"] = request.user.id  
        data["application_id"] = generate_application_id() 

        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            serializer.save(user=request.user, application_id=data["application_id"])
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CurrencyListView(views.APIView):
    def get(self, request, *args, **kwargs):
        base = request.query_params.get("base")

        rates_qs = Rates.objects.select_related("currency_f", "currency_t")
        if base:
            rates_qs = rates_qs.filter(currency_f__currency=base)

        networks_by_code = defaultdict(list)
        for f in Finance.objects.all():
            networks_by_code[f.currency].append(f)

        data = RatesSerializer(
            rates_qs,
            many=True,
            context={"request": request, "networks_by_code": networks_by_code},
        ).data

        if base:
            targets = [
                {
                    "pair_id": item["id"],
                    "target_currency": item["target_currency"],
                    "rate": item["rate"],
                    "fixed": item['fixed'],
                    "min_amount": item["min_amount"],
                    "max_amount": item["max_amount"],
                    "updated_at": item["updated_at"],
                }
                for item in data
            ]
            return Response({"targets": targets})

        currencies = Finance.objects.distinct("currency")
        currencies_data = CurrencySerializer(
            currencies, many=True, context={"request": request, "networks_by_code": networks_by_code}
        ).data

        return Response({"currencies": currencies_data})

class MarketsView(views.APIView):
    def get(self, request):
        client = WhiteBitClient()
        try:
            data = client.get_markets()
            return Response(data, status=status.HTTP_200_OK)
        except ConnectionError as e:
            return Response({"error": str(e)})


class TickerView(views.APIView):
    def get(self, request):
        client = WhiteBitClient()
        try:
            data = client.get_ticker()
            return Response(data, status=status.HTTP_200_OK)
        except ConnectionError as e:
            return Response({"error": str(e)}, status=status.HTTP_503_SERVICE_UNAVAILABLE)


class FeeView(views.APIView):

    def get(self, request):
        client = WhiteBitClient()
        try:
            data = client.get_fee()
            return Response(data, status=status.HTTP_200_OK)
        except ConnectionError as e:
            return Response({"error": str(e)}, status=status.HTTP_503_SERVICE_UNAVAILABLE)


