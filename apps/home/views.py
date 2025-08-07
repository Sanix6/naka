from django.shortcuts import render
from rest_framework import generics, views
from rest_framework.response import Response
from . import models, serializers
from rest_framework.permissions import IsAuthenticated

class NewsView(views.APIView):
    def get(self, request, *args, **kwargs):
        news = models.News.objects.all()
        serializer = serializers.NewsSerializer(news, many=True)
        return Response(serializer.data)
    
class NewsContentView(generics.RetrieveAPIView):
    queryset = models.News.objects.all()
    serializer_class = serializers.NewsContentSerializer
    lookup_field = 'slug'
    
    def get(self, request, *args, **kwargs):
        news = self.get_object()
        serializer = self.get_serializer(news)
        return Response(serializer.data)

class FeedBackView(generics.ListAPIView):
    queryset = models.FeedBack.objects.all()
    serializer_class = serializers.FeedBackSerializer

class FeedBackSendView(generics.GenericAPIView):
    serializer_class = serializers.FeedBackSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(name=request.user)
        return Response(serializer.data, status=201)




class FAQView(generics.ListAPIView):
    queryset = models.FAQ.objects.all()
    serializer_class = serializers.FAQSerializer

    def get(self, request, *args, **kwargs):
        faqs = self.get_queryset()
        serializer = self.get_serializer(faqs, many=True)
        return Response(serializer.data)