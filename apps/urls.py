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
    url(r'^set_user_password/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.ChangeForgetPassword.as_view(), name='change_forget_password'),
    url(r'^home/profile/change_password/$', views.ChangePassword.as_view(), name='profile-change-password'),
    url(r'^set_password/$', views.SetPassword.as_view(), name='set_password'),
    url(r'^forget_password/$', views.ForgetPassword.as_view(), name='forget_password'),
    url(r'^home/category/$', views.CategoryList.as_view(), name='category_list'),
    # url(r'^home/category/(?P<category>\w+)/practice/(?P<level>\w+)/$', views.PlayQuiz.as_view(), name='play_game'),
    url(r'^home/category/(?P<category>\w+)/practice/(?P<level>\w+)/instruction/$', views.Instruction.as_view(), name='instruction'),
    url(r'^home/category/(?P<category>\w+)/practice/(?P<level>\w+)/start/(?P<pk>[0-9]+)/$', views.PlayQuiz.as_view(), name='instruction'),
    # url(r'^home/category/(?P<category>\w+)/compete/$', views.PlayQuizCompete.as_view(), name='play_game'),
])

# urlpatterns += [
#     url(r'^', include(router.urls)),
# ]
