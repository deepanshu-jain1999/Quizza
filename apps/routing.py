from django.urls import re_path
from django.conf.urls import url
from . import consumers

websocket_urlpatterns = [
    url(r"^home/category/(?P<category>\w+)/compete/$", consumers.CollectConsumer),

]

