from rest_framework import serializers
from . import models
import re
from bs4 import BeautifulSoup

class NewsContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.News
        fields = ('content', )


class NewsSerializer(serializers.ModelSerializer):
    content_q = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField(format="%Y-%m-%d", read_only=True)

    class Meta:
        model = models.News
        fields = ('slug', 'title', 'content_q', 'image', 'created_at')
        read_only_fields = ('id', 'created_at')

    
    def get_content_q(self, obj):
        soup = BeautifulSoup(obj.content, "html.parser")
        text = soup.get_text(separator=" ", strip=True) 
        
        words = text.split()
        short_text = ' '.join(words[:50])
        return short_text