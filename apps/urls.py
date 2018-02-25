from django.conf.urls import include, url
from apps import views
from django.contrib.auth import views as built_views

urlpatterns = [
    url(r'^signup/$', views.Signup.as_view(), name='signup'),
    url(r'^activate_user/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.Activate.as_view(), name='activate'),
    url(r'^login/$', views.Login.as_view(), name='login'),
    url(r'^logout/$', built_views.logout, {'next_page': 'login'}, name='logout'),
]