from channels.generic.websocket import JsonWebsocketConsumer
import json
from rest_framework import permissions, generics
from rest_framework.authentication import TokenAuthentication
from .models import CompeteQuiz, Category
import time
from asgiref.sync import async_to_sync

current_time = time.time()
x = 0
method = 0


class CollectConsumer(JsonWebsocketConsumer):

    def get_question(self, cat, i):
        cat_obj = Category.objects.get(category=cat)
        quiz = CompeteQuiz.objects.filter(category=cat_obj)[i]
        quiz = quiz.for_json()
        return quiz

    def connect(self):
        global method
        global x
        if method == 1:
            self.close()
        self.accept()

    def receive(self, **kwargs):
        global x, method, current_time
        x += 1
        print("1-->", current_time, x)
        if x < 2:
            current_time = time.time()
        # if time.time()-current_time-20 > 0:
        #     method = 1

        print("2-->", current_time, x, method)
        time.sleep(current_time+10-time.time())
        cat = self.scope["url_route"]["kwargs"]["category"]
        cat_obj = Category.objects.get(category=cat)
        time_per_ques = cat_obj.compete_time
        total_ques = CompeteQuiz.objects.filter(category=cat_obj).count()
        for i in range(total_ques):
            d = self.get_question(cat, i)
            time.sleep(time_per_ques)
            self.send(text_data=json.dumps({
                'message': d
            }))

    def disconnect(self, code):
        global x, method
        x -= 1
        if x == 0:
            method = 0
        self.close()

    # def receive(self, text_data, **kwargs):
    #     # from_time = time.time()
    #     print(self.current_time)
    #     if self.x < 2:
    #         self.current_time = time.time()
    #     cat = self.scope["url_route"]["kwargs"]["category"]
    #     d = self.get_question(cat)
    #     time.sleep(time.time()+20-self.current_time)
    #     async_to_sync(self.channel_layer.group_send)(
    #         "player",
    #         {
    #             "type": "player.question",
    #             "text": json.dumps(d),
    #         },
    #     )




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

    # def player_question(self, event):
    #     self.send(text_data=event["text"])


