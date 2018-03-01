from django.conf.urls import include, url
from django.contrib import admin
from . import settings
from django.conf.urls.static import static


urlpatterns = [
    # Examples:
    # url(r'^$', 'quizup.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', admin.site.urls),
    url(r'^', include('apps.urls'))
]+  static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
