from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

urlpatterns = [
    path('rent/', include('rent.urls')),
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(url='rent/', permanent=True)),
] + (static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT))
