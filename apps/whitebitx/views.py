from django.shortcuts import render
from rest_framework import generics, status, views, permissions
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from connectors.public.client import WhiteBitClient, WhiteBitPrivateClient
from collections import defaultdict
from .serializers import *
from assets.services.generator import generate_application_id
import os
from django.utils import timezone
from datetime import timedelta


class CryptoDepositAddressGenericView(generics.GenericAPIView):
    serializer_class = CryptoDepositAddressSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        application_id = serializer.validated_data['application_id']
        invoice_to = serializer.validated_data['invoice_to']

        try:
            transaction = HistoryTransactions.objects.get(application_id=application_id)
        except HistoryTransactions.DoesNotExist:
            return Response(
                {"error": "Заявка не найдена"},
                status=status.HTTP_404_NOT_FOUND
            )

        ticker = transaction.currency_from.currency 
        network = transaction.currency_from.network

        public_key = os.getenv('public_key')
        secret_key = os.getenv('secret_key')
        client = WhiteBitPrivateClient(public_key, secret_key)

        result = client.get_address(ticker, network)

        if 'error' in result:
            return Response(result, status=status.HTTP_400_BAD_REQUEST)

        invoice_from = result.get("account", {}).get("address")

        transaction.invoice_from = invoice_from
        transaction.invoice_to = invoice_to
        transaction.expired = timezone.now() + timedelta(minutes=60) 
        transaction.save(update_fields=["invoice_from", "invoice_to", "expired"])

        full_data = HistoryTransactionSerializer(transaction).data
        return Response(full_data, status=status.HTTP_200_OK)


class TransactionsListView(generics.ListAPIView):
    serializer_class = HistoryTransactionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return HistoryTransactions.objects.filter(user=self.request.user).order_by('-created_at')


class TransactionHistoryView(generics.GenericAPIView):
    serializer_class = TransactionHistorySerializers
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        
        if serializer.is_valid():
            transaction_method = serializer.validated_data['transactionMethod']
            address = serializer.validated_data.get('address')
            unique_id = serializer.validated_data.get('uniqueId')
            # status_list = serializer.validated_data.get('status')

            client = WhiteBitPrivateClient(public_key='45f78aa66fb498abdae7c3883fb57ccd', secret_key='c27bb4c14b1e9eaff868548c1ff76d04')

            history_data = client.get_history(
                transactionMethod=transaction_method,
                address=address,
                uniqueId=unique_id,
                # status=status_list
            )

            if 'error' in history_data:
                return Response(history_data, status=status.HTTP_400_BAD_REQUEST)

            return Response(history_data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CreateApplicationView(generics.GenericAPIView):
    serializer_class = CreateApplicationSerializer
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


class GETBalance(views.APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        client = WhiteBitPrivateClient(public_key='45f78aa66fb498abdae7c3883fb57ccd', secret_key='c27bb4c14b1e9eaff868548c1ff76d04')
        balance = client.get_balance()  
        return Response(balance)

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


class StatusView(generics.GenericAPIView):
    serializer_class = HistoryTransactionSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        application_id = request.query_params.get("application_id")
        if not application_id:
            return Response({"error": "application_id is required"}, status=400)

        queryset = HistoryTransactions.objects.filter(application_id=application_id)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)









































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


