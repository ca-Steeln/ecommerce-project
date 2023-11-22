
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', include('exceptions.urls')),
    path('', include('pages.urls')),
    path('', include('registration.urls')),
    path('', include('htmx_messages.urls')),
    path('moderation/', include('moderation.urls')),
    path('accounts/', include('accounts.urls')),
    path('search', include('searches.urls')),
    path('categories/', include('categories.urls')),
    path('products/', include('products.urls')),
    path('accounts/<int:pk>/inventory/', include('inventories.urls')),
    path('accounts/<int:pk>/orders/', include('orders.urls')),
    path('dashboard/', include('dashboard.urls')),

    # security :
    # change this route "administration/" in production
    path('administration/', include('administration.urls')),
    path('admin/', admin.site.urls),
]

urlpatterns += static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
)

handler404 = 'exceptions.views.exception_404_view'
