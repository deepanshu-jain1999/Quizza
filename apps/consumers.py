from channels.generic.websocket import JsonWebsocketConsumer
import json
from rest_framework import permissions, generics
from rest_framework.authentication import TokenAuthentication
from .models import CompeteQuiz, Category, User, CompeteScore
import time
from asgiref.sync import async_to_sync
from rest_framework.authtoken.models import Token


current_time = time.time()
x = 0
method = 0
tk = {}

class CollectConsumer(JsonWebsocketConsumer):

    def get_question(self, cat, i):
        cat_obj = Category.objects.get(category=cat)
        quiz = CompeteQuiz.objects.filter(category=cat_obj)[i]
        quiz = quiz.for_json()
        return quiz

    def disconnect(self, code=None):
        global x, method
        x -= 1
        print("x in dis", x)
        if x == 0:
            method = 0
        self.close()

    def connect(self):
        global method, x
        if method == 1:
            self.disconnect()
        x += 1
        self.accept()

    def receive(self, text_data, **kwargs):
        global x, method, current_time, tk
        if x < 2:
            current_time = time.time()
        a = current_time+10-time.time()
        if a < 0:
            method = 1
            self.send(text_data=json.dumps({
                "status": "no",
                "message": "try after some time",
            }))
            return self.disconnect()

        time.sleep(a)
        cat = self.scope["url_route"]["kwargs"]["category"]
        cat_obj = Category.objects.get(category=cat)
        time_per_ques = cat_obj.compete_time
        total_ques = CompeteQuiz.objects.filter(category=cat_obj).count()
        # text_data_json = json.loads(text_data)
        # token = text_data_json['message']
        # score = text_data_json['result']
        # per_score = (score / total_ques) * 100
        # tk[token] = score
        for i in range(total_ques):
            d = self.get_question(cat, i)
            time.sleep(time_per_ques)
            self.send(text_data=json.dumps({
                "status": "yes",
                "question": d["question"],
                "option1": d["option1"],
                "option2": d["option2"],
                "option3": d["option3"],
                "option4": d["option4"],
                "answer": d["answer"],

            }))
        time.sleep(time_per_ques)
        self.send(text_data=json.dumps({
            "status": "done",
        }))

        self.disconnect()




































        # token_obj = Token.objects.get(token=token)
        # print(token_obj)
        # user = User.objects.get(key=token_obj)
        # obj = CompeteScore.objects.get_or_create(user=user, category=cat_obj)
        # print(user.username)
        # if per_score>obj.compete_score:
        #     obj.compete_score = per_score
        # obj.save()
        # tk.remove(token)
        # self.disconnect()



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

