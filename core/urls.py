from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('api/admin/', admin.site.urls),
    path("api/auth/", include("apps.users.urls")),
    path("api/base/", include("apps.home.urls")),
    path("api/v4/", include("apps.whitebitx.urls")),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/backarea/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("api/schema/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
    path('ckeditor/', include('ckeditor_uploader.urls')), 

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
