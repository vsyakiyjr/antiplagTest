
from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static

from . import settings

# from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('checker/', include('checker.urls',namespace='checker')),
    path('avoid/', include('avoid.urls', namespace='avoid')),
    path('reports/', include('reports.urls', namespace='reports')),
    path('auth/', include('users.urls', namespace='users')),
    path('auth/', include('django.contrib.auth.urls')),
    path('users', include('users.urls', namespace='users'))
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )