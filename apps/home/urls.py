from django.urls import path, include
from . import views
from .views import ImagesListView
from django.conf.urls.static import static
import os
from django.conf import settings



urlpatterns = [
    path('news/', views.NewsView.as_view(), name='news'),
    path('news/<slug:slug>/', views.NewsContentView.as_view(), name='news_content'),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('feedback/', views.FeedBackView.as_view(), name='feedback'),
    path('feedback/send/', views.FeedBackSendView.as_view(), name='feedback_send'),
    path('faq/', views.FAQView.as_view(), name='faq'),
    
    path('images/', ImagesListView.as_view(), name='images_list'),
]


