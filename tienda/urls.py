from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),        # Panel de Django
    path('', include('productos.urls')),    # Todas las rutas de la tienda
]

# En desarrollo: permite ver las imagenes subidas a media/
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)