from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    # path('', include('users.urls')),  # Đã comment lại vì không có users/urls.py
    path('reminders/', include('reminders.urls')),
    path('bills/', include('bills.urls')),
    path('roommates/', include('roommates.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
