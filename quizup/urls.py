from django.urls import include, path
from django.contrib import admin
from . import settings
from django.conf.urls.static import static
from rest_framework.documentation import include_docs_urls


urlpatterns = [
    path('/admin/', admin.site.urls),
    # path('/api/', include('apps.urls')),

 ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += [
    path('docs/', include_docs_urls(title='Quizza api docs'))
]