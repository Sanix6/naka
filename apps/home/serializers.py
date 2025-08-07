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
    created_at = serializers.SerializerMethodField()

    class Meta:
        model = models.News
        fields = ('id','slug', 'title', 'content_q', 'image', 'created_at', 'url')
        read_only_fields = ('id', 'created_at')

    
    def get_content_q(self, obj):
        soup = BeautifulSoup(obj.content, "html.parser")
        text = soup.get_text(separator=" ", strip=True) 
        
        words = text.split()
        short_text = ' '.join(words[:50])
        return short_text

    def get_image(self, obj):
        request = self.context.get('request')
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        return None

    def get_created_at(self, obj):
        return obj.created_at.strftime("%Y-%m-%d")


class FeedBackSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    created_at = serializers.SerializerMethodField()
    class Meta:
        model = models.FeedBack
        fields = ('id', 'name', 'star', 'text', 'created_at')
        read_only_fields = ('id', 'created_at')

    def get_name(self, obj):
        return obj.name.first_name


    def validate_text(self, value):
        if not value.strip():
            raise serializers.ValidationError("Сообщение не может быть пустым.")
        return value

    def get_created_at(self, obj):
        return obj.created_at.strftime("%Y-%m-%d %H:%M:%S")


class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.FAQ
        fields = ('id', 'question', 'answer', 'created_at')
    