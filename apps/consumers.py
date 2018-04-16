from channels.generic.websocket import JsonWebsocketConsumer
import json
from rest_framework import permissions, generics
from rest_framework.authentication import TokenAuthentication
from .models import CompeteQuiz, Category
import time
from asgiref.sync import async_to_sync


class CollectConsumer(JsonWebsocketConsumer):
    # permission_classes = (permissions.IsAuthenticated,)
    # authentication_classes = (TokenAuthentication,)
    current_time = time.time()
    x = 0

    def get_question(self, cat):
        cat_obj = Category.objects.get(category=cat)
        quiz = CompeteQuiz.objects.filter(category=cat_obj)
        quiz = [quiz_obj.for_json() for quiz_obj in quiz]
        return quiz

    def connect(self):
        async_to_sync(self.channel_layer.group_add)("player", self.channel_name)
        self.x += 1
        self.accept()

    def receive(self, text_data, **kwargs):
        # from_time = time.time()
        print(self.current_time)
        if self.x < 2:
            self.current_time = time.time()
        cat = self.scope["url_route"]["kwargs"]["category"]
        d = self.get_question(cat)
        time.sleep(time.time()+20-self.current_time)
        async_to_sync(self.channel_layer.group_send)(
            "player",
            {
                "type": "player.question",
                "text": json.dumps(d),
            },
        )
        # print()
        # self.lt.append("1")
        # text_data_json = json.loads(text_data)
        # cat = self.scope["url_route"]["kwargs"]["category"]
        # token = str(text_data_json['token'])
        # time = int(text_data_json['time'])
        # self.lt.append(token)
        # if len(self.lt)==1:
        #     self.current_time = time
        #
        # d = self.get_question(cat)
        # # print(self.current_time+20-time.time())
        # time.sleep(int(self.current_time)+20-time.time())
        # print(self.lt)
        # print(self.current_time)
        # self.send(text_data=json.dumps({
        #     'message': d
        # }))

    def player_question(self, event):
        self.send(text_data=event["text"])

    def disconnect(self, code):
        self.x -= 1
        async_to_sync(self.channel_layer.group_discard)("player", self.channel_name)

