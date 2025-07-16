from django.shortcuts import render
from rest_framework import generics, views
from rest_framework.response import Response
from . import models, serializers

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