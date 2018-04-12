from django.urls import include, re_path
from apps import views
from django.contrib.auth import views as built_views
from rest_framework.routers import DefaultRouter
from rest_framework.urlpatterns import format_suffix_patterns

#
# # router = DefaultRouter()
# # router.register(r'home/profile', views.ProfileViewSet, base_name='profile')
#
#
urlpatterns = format_suffix_patterns([
    # url(r'^', include(router.urls)),
    re_path(r'^signup/$', views.Signup.as_view(), name='signup'),
    re_path(r'^activate_user/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.Activate.as_view(), name='activate'),
    re_path(r'^login/$', views.Login.as_view(), name='login'),
    re_path(r'^logout/$', built_views.logout, {'next_page': 'login'}, name='logout'),
    re_path(r'^home/profile/$', views.UserProfile.as_view(), name='profile-list'),
    re_path(r'^set_user_password/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.ChangeForgetPassword.as_view(), name='change_forget_password'),
    re_path(r'^home/profile/change_password/$', views.ChangePassword.as_view(), name='profile-change-password'),
    re_path(r'^set_password/$', views.SetPassword.as_view(), name='set_password'),
    re_path(r'^forget_password/$', views.ForgetPassword.as_view(), name='forget_password'),
    re_path(r'^home/category/$', views.CategoryList.as_view(), name='category_list'),
    re_path(r'^home/category/(?P<category>\w+)/practice/(?P<level>\w+)/instruction/$', views.Instruction.as_view(), name='instruction'),
    re_path(r'^home/category/(?P<category>\w+)/practice/(?P<level>\w+)/start/(?P<pk>[0-9]+)/$', views.PlayQuiz.as_view(), name='start_game'),
    re_path(r'^home/category/(?P<category>\w+)/practice/(?P<level>\w+)/result/$', views.GetScore.as_view(), name='result'),
])

urlpatterns += [
    re_path(r'^home/category/(?P<category>\w+)/compete/$', views.CompeteQuizView.as_view(), name='compete_game'),
]

