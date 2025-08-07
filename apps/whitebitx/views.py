from django.shortcuts import render
from rest_framework import generics, status, views
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from connectors.public.client import WhiteBitClient


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
    permission_classes = [IsAuthenticated]

    def get(self, request):
        client = WhiteBitClient()
        try:
            data = client.get_fee()
            return Response(data, status=status.HTTP_200_OK)
        except ConnectionError as e:
            return Response({"error": str(e)}, status=status.HTTP_503_SERVICE_UNAVAILABLE)