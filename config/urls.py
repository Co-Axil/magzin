from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

from rest_framework import permissions
# Swagger dokumentatsiya

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('', include('onlinemarket.urls')),
    path('users/', include('users.urls')),
    path('', include('admin_tabler.urls')),
    path('', TemplateView.as_view(template_name="base.html"), name="home"),  # Bosh sahifa
    path('products/', include('onlinemarket.urls')),  # App uchun URLlar

    
    # Admin panel
    path('admin/', admin.site.urls),
    
    # Asosiy ilova (onlinemarket)
     path('', include('onlinemarket.urls')),
    path('products/', include('onlinemarket.urls')),  # Agar alohida products/ prefiksi kerak bo'lsa
    
    # Foydalanuvchilar ilovasi
    path('users/', include('users.urls')),
    
    # Admin tabler uchun URLlar
    path('', include('admin_tabler.urls')),
    
    # Bosh sahifa
    path('', TemplateView.as_view(template_name="base.html"), name="home"),
]

# Faqat development rejimida media fayllar uchun
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)