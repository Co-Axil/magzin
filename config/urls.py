from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Swagger uchun schema sozlamalari
schema_view = get_schema_view(
    openapi.Info(
        title="OnlineMarket API",
        default_version='v1',
        description="API Documentation",
        terms_of_service="https://yourapp.com/terms/",
        contact=openapi.Contact(email="contact@magzin.com"),
    public=True,
    permission_classes=(permissions.AllowAny,),
))

urlpatterns = [
    # Swagger dokumentatsiya
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    
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