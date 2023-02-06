from django.conf import settings
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('customer.urls')),
    path('management/', include('management.urls')),
    path('auth/', include('user_model.urls'), name='admin'),
    path('auth/', include('django.contrib.auth.urls')),
    path('accounts/', include('allauth.urls')),
]

if settings.DEBUG:
    urlpatterns = [path('__debug__/', include('debug_toolbar.urls')), ] + urlpatterns
