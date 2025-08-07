from django.urls import path, include
from . import views

urlpatterns = [
    path('news/', views.NewsView.as_view(), name='news'),
    path('news/<slug:slug>/',views.NewsContentView.as_view(), name='news_content'),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('feedback/', views.FeedBackView.as_view(), name='feedback'),
    path('feedback/send/', views.FeedBackSendView.as_view(), name='feedback_send'),
    path('faq/', views.FAQView.as_view(), name='faq'),

]

