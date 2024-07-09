from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from wagtail import urls as wagtail_urls
from wagtail.admin import urls as wagtailadmin_urls
from wagtail.documents import urls as wagtaildocs_urls

from django.contrib import admin

urlpatterns = [
    path('django-admin/', admin.site.urls),  # Django admin
    path('admin/', include(wagtailadmin_urls)),  # Wagtail admin  
    path('documents/', include(wagtaildocs_urls)),
    path('cart/', include('cart.urls', namespace='cart')),
    path('orders/', include('orders.urls', namespace='orders')),
    path('service/', include('service.urls', namespace='service')),
    path('', include('shop.urls', namespace='shop')),
    path('', include(wagtail_urls)),  # Wagtail pages serve
]

#if settings.DEBUG:
   # urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

