from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.i18n import JavaScriptCatalog

urlpatterns = [
    path('admin/', admin.site.urls),
    path('jsi18n/', JavaScriptCatalog.as_view(), name='javascript-catalog'),
    path('summernote/', include('django_summernote.urls')),

    path('', include('static_pages.urls')),
    path('users/', include('users.urls')),
    path('catalog/', include('catalog.urls')),
    path('payment/', include('payment.urls')),
]

if settings.DEBUG:
    if settings.STATIC_ROOT:
        urlpatterns += static(
            settings.STATIC_URL, document_root=settings.STATIC_ROOT
            )
    if settings.MEDIA_ROOT:
        urlpatterns += static(
            settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
            )

    urlpatterns += [path('__debug__/', include('debug_toolbar.urls'))]
