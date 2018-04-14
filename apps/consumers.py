from channels.generic.websocket import JsonWebsocketConsumer
import json
from rest_framework import permissions, generics
from rest_framework.authentication import TokenAuthentication
from .models import CompeteQuiz, Category


class PlayConsumer(JsonWebsocketConsumer):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)


    def get_question(self, cat):
        cat_obj = Category.objects.get(category=cat)
        quiz = CompeteQuiz.objects.filter(category=cat_obj)
        quiz = [quiz_obj.for_json() for quiz_obj in quiz]
        return quiz

    # def get_queryset(self):
    #     cat = self.scope["url_route"]["kwargs"]["category"]
    #     print(cat)
    #     cat_obj = Category.objects.get(category=cat)
    #     quiz = CompeteQuiz.objects.filter(category=cat_obj)
    #     print(quiz)
    #     return quiz

    # def connect(self, **kwargs):
    #     pass
    #
    #

    def receive(self, text_data, **kwargs):
        text_data_json = json.loads(text_data)
        cat = self.scope["url_route"]["kwargs"]["category"]
        message = text_data_json['message']
        print(message)
        d = self.get_question(cat)
        self.send(text_data=json.dumps({
            'message': d
        }))


    # def disconnect(self, **kwargs):
    #     pass