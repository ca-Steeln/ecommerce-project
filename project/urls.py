
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', include('registration.urls')),
    path('', include('pages.urls')),
    path('', include('htmx_messages.urls')),
    path('accounts/', include('accounts.urls')),
    path('categories/', include('categories.urls')),
    path('categories/<str:category_name>/products/', include('products.urls')),
    path('accounts/<int:client_pk>/inventory/', include('inventories.urls')),
    path('accounts/<int:client_pk>/orders/', include('orders.urls')),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )

