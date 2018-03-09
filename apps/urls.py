from django.conf.urls import include, url
from apps import views
from django.contrib.auth import views as built_views
from rest_framework.routers import DefaultRouter
from rest_framework.urlpatterns import format_suffix_patterns


# router = DefaultRouter()
# router.register(r'home/profile', views.ProfileViewSet, base_name='profile')


urlpatterns = format_suffix_patterns([
    # url(r'^', include(router.urls)),
    url(r'^signup/$', views.Signup.as_view(), name='signup'),
    url(r'^activate_user/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.Activate.as_view(), name='activate'),
    url(r'^login/$', views.Login.as_view(), name='login'),
    url(r'^logout/$', built_views.logout, {'next_page': 'login'}, name='logout'),
    url(r'^home/profile/$', views.ProfileList.as_view(), name='profile-list'),
    url(r'^home/profile/(?P<pk>[0-9]+)/$', views.ProfileDetail.as_view(), name='profile-detail'),
    # url(r'^home/profile/$', views.ProfileList.as_view(), name='profile-list'),
    # url(r'^home/category/practice/$', views.PracticeMode.as_view(), name='practice_mode'),
    # url(r'^home/category/competitive/$', views.CompetitiveMode.as_view(), name='competitive_mode'),
])
# urlpatterns = (urlpatterns)

# urlpatterns += [
#     url(r'^', include(router.urls)),
# ]
