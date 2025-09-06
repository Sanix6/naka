from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from django.conf import settings
from django.conf.urls.static import static
from apps.whitebitx.views import *


urlpatterns = [
    path('api/admin/', admin.site.urls),
    path("api/auth/", include("apps.users.urls")),
    path("api/base/", include("apps.home.urls")),
    path("api/v4/", include("apps.whitebitx.urls")),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/backarea/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("api/schema/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
    path('ckeditor/', include('ckeditor_uploader.urls')), 

    #private
    path('api/private/main-balance', GETBalance.as_view(), name="private"),
    path('api/private/trade-balance', GETTradeBalance.as_view(), name="private"),
    path('api/private/transaction-history/', TransactionHistoryView.as_view(),  name="private"),
    path('api/private/withdraw', WithdrawView.as_view(),name="private"),
    path("api/private/trade-history", GETTradeHistory.as_view(),name="private"),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
