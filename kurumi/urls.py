
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('features', TemplateView.as_view(template_name='features.html'), name='features'),
    path('pricing', TemplateView.as_view(template_name='pricing.html'), name='pricing'),
    path('contact', TemplateView.as_view(template_name='contact.html'), name='contact'),
    path('faq', TemplateView.as_view(template_name='faq.html'), name='faq'),
    path('about', TemplateView.as_view(template_name='about.html'), name='about'),
    path('blog', TemplateView.as_view(template_name='blog.html'), name='blog'),
    path('careers', TemplateView.as_view(template_name='careers.html'), name='careers'),
    path('help', TemplateView.as_view(template_name='help.html'), name='help'),
    path('privacy', TemplateView.as_view(template_name='privacy.html'), name='privacy'),
    path('terms', TemplateView.as_view(template_name='terms.html'), name='terms'),
    # path('reminders/', include('reminders.urls')),  # Đã comment lại vì không có reminders/urls.py
    # path('bills/', include('bills.urls')),
    # path('roommates/', include('roommates.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
