from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('onlinemarket.urls')),
    path('users/', include('users.urls')),
    path('', include('admin_tabler.urls')),
      path('', TemplateView.as_view(template_name="base.html"), name="home"),  # Bosh sahifa
    path('products/', include('onlinemarket.urls')),  # App uchun URLlar
    
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
