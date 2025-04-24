from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from drf_yasg.views import get_schema_view
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
schema_view = get_schema_view(
    openapi.Info(
        title="My API",
        default_version='v1',
        description="API documentation",
    ),
    public=True,
)
urlpatterns = [
    path('admin/', admin.site.urls),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('swagger/', SpectacularSwaggerView.as_view(url_name='schema')),
    path('swagger<format>/', schema_view.without_ui()),  # JSON/YAML format
    path('swagger/', schema_view.with_ui('swagger')),
    path('', include('onlinemarket.urls')),
    path('users/', include('users.urls')),
    path('', include('admin_tabler.urls')),
      path('', TemplateView.as_view(template_name="base.html"), name="home"),  # Bosh sahifa
    path('products/', include('onlinemarket.urls')),  # App uchun URLlar
    
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
