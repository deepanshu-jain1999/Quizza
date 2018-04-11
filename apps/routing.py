from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r'^home/category/(?P<category>\w+)/compete/$', consumers.PlayConsumer),
]
