from channels.generic.websocket import JsonWebsocketConsumer
import json
from rest_framework import permissions, generics
from rest_framework.authentication import TokenAuthentication


class PlayConsumer(JsonWebsocketConsumer):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def connect(self, **kwargs):
        print(**kwargs)

    def disconnect(self, **kwargs):
        print(**kwargs)

    def receive(self, **kwargs):
        print(**kwargs)
