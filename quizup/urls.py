from django.urls import include, path
from django.conf.urls import url
from django.contrib import admin
from . import settings
from django.conf.urls.static import static
from rest_framework.documentation import include_docs_urls


urlpatterns = [
    path(r'admin/', admin.site.urls),
    path(r'', include('apps.urls')),
    url(r'^docs/', include_docs_urls(title='Quizza api docs'))

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url(r'^debug_tool/', include(debug_toolbar.urls)),
    ] + urlpatterns

