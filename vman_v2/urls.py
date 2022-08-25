from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('vman2_tz_admin/', admin.site.urls),
    path('', include('dashboard.urls', namespace = 'candidate')),
    path('authentication/', include('authentication.urls', namespace = 'authentication')),
]
urlpatterns += static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)
