from django.conf.urls import include, url
from apps import views

urlpatterns = [
    url(r'^signup/$', views.Signup.as_view(), name='signup'),

    # url(r'^signup/$', views.Signup.as_view()),
]