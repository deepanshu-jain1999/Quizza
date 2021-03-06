from channels.generic.websocket import JsonWebsocketConsumer
import json
from rest_framework import permissions, generics
from rest_framework.authentication import TokenAuthentication
from .models import CompeteQuiz, Category, User, CompeteScore
import time
from asgiref.sync import async_to_sync
from rest_framework.authtoken.models import Token
import operator


current_time = time.time()
x = 0
method = 0
dict_user_score = {}


class CollectConsumer(JsonWebsocketConsumer):
    def sort_result(self, dict_user_score):
        sorted_dict = [(k, dict_user_score[k]) for k in sorted(dict_user_score, key=dict_user_score.get, reverse=True)]
        print(sorted_dict)
        d = {}
        for c in sorted_dict:
            d[c[0]] = c[1]
        print(d)
        return [d]

    def token_to_user(self, token):
        token_obj = Token.objects.get(key=token)
        user = token_obj.user
        print(user)
        return user

    def get_question(self, cat, i):
        cat_obj = Category.objects.get(category=cat)
        quiz = CompeteQuiz.objects.filter(category=cat_obj)[i]
        quiz = quiz.for_json()
        return quiz

    def disconnect(self, code=None):
        global x, method, dict_user_score
        x -= 1
        print("x in dis", x)
        async_to_sync(self.channel_layer.group_discard)("player", self.channel_name)
        if x == 0:
            dict_user_score = {}
            method = 0
        self.close()

    def connect(self):
        print("connect")
        global method, x
        if method == 1:
            self.disconnect()
        self.accept()

    def player_message(self, event):
        self.send(text_data=event["text"])


    def receive(self, text_data, **kwargs):

        global x, method, current_time, dict_user_score
        text_data_json = json.loads(text_data)
        token = text_data_json['message']
        user = self.token_to_user(token)
        username = str(user.username)
        score = text_data_json['result']
        dict_user_score[str(self.token_to_user(token).username)]= text_data_json['result']
        if score != -5:
            print("-->",username, score)
            # dict_user_score[username] = score

            # async_to_sync(self.channel_layer.group_send)(
            #     "player",
            #     {
            #         "type": "player.message",
            #         "text": json.dumps({"resArray":score, "result": username}),
            #         # "score": score,
            #         # "text": self.sort_result(dict_user_score),
            #     },
            # )
            time.sleep(5)
            self.send(text_data=json.dumps({
                "status": "your score",
                "resArray": self.sort_result(dict_user_score),
            }))
            # return self.disconnec
            print("dict",dict_user_score)
            return 0

        x += 1
        print(x)
        if x == 1:
            current_time = time.time()
        a = current_time+4-time.time()
        if a < 0:
            method = 1
            self.send(text_data=json.dumps({
                "status": "no",
                "message": "try after some time",
            }))
            # return self.disconnect()

        time.sleep(a)
        cat = self.scope["url_route"]["kwargs"]["category"]
        cat_obj = Category.objects.get(category=cat)
        time_per_ques = cat_obj.compete_time
        total_ques = CompeteQuiz.objects.filter(category=cat_obj).count()
        # text_data_json = json.loads(text_data)
        token = text_data_json['message']
        # score = text_data_json['result']
        # per_score = (score / total_ques) * 100
        # tk[token] = score
        async_to_sync(self.channel_layer.group_add)("player", self.channel_name)
        dict_user_score[username] = 0

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











# previous method

    #     from channels.generic.websocket import JsonWebsocketConsumer
    #     import json
    #     from rest_framework import permissions, generics
    #     from rest_framework.authentication import TokenAuthentication
    #     from .models import CompeteQuiz, Category, User, CompeteScore
    #     import time
    #     from asgiref.sync import async_to_sync
    #     from rest_framework.authtoken.models import Token
    #
    #     current_time = time.time()
    #     x = 0
    #     method = 0
    #     tk = {}
    #
    #     class CollectConsumer(JsonWebsocketConsumer):
    #
    #         def get_question(self, cat, i):
    #             cat_obj = Category.objects.get(category=cat)
    #             quiz = CompeteQuiz.objects.filter(category=cat_obj)[i]
    #             quiz = quiz.for_json()
    #             return quiz
    #
    #         def connect(self):
    #             global method
    #             global x
    #             if method == 1:
    #                 self.close()
    #             self.accept()
    #
    #         def receive(self, text_data, **kwargs):
    #             global x, method, current_time, tk
    #             print("x->", x)
    #             x += 1
    #             print("x->", x)
    #             # print("1-->", current_time, x)
    #             if x < 2:
    #                 current_time = time.time()
    #             # if time.time()-current_time-20 > 0:
    #             #     method = 1
    #             # print("2-->", current_time, x, method)
    #             a = current_time + 10 - time.time()
    #             if a < 0:
    #                 method = 1
    #                 self.send(text_data=json.dumps({
    #                     "status": "no",
    #                     "message": "try after some time",
    #                 }))
    #                 x -= 1
    #                 self.close()
    #                 return 0
    #             time.sleep(current_time + 10 - time.time())
    #             cat = self.scope["url_route"]["kwargs"]["category"]
    #             cat_obj = Category.objects.get(category=cat)
    #             time_per_ques = cat_obj.compete_time
    #             total_ques = CompeteQuiz.objects.filter(category=cat_obj).count()
    #             text_data_json = json.loads(text_data)
    #             token = text_data_json['message']
    #             score = text_data_json['result']
    #             per_score = (score / total_ques) * 100
    #             tk[token] = score
    #             for i in range(total_ques):
    #                 d = self.get_question(cat, i)
    #                 time.sleep(time_per_ques)
    #                 self.send(text_data=json.dumps({
    #                     "status": "yes",
    #                     "question": d["question"],
    #                     "option1": d["option1"],
    #                     "option2": d["option2"],
    #                     "option3": d["option3"],
    #                     "option4": d["option4"],
    #                     "answer": d["answer"],
    #
    #                 }))
    #             time.sleep(time_per_ques)
    #             self.send(text_data=json.dumps({
    #                 "status": "done",
    #             }))
    #             # token_obj = Token.objects.get(token=token)
    #             # print(token_obj)
    #             # user = User.objects.get(key=token_obj)
    #             # obj = CompeteScore.objects.get_or_create(user=user, category=cat_obj)
    #             # print(user.username)
    #             # if per_score>obj.compete_score:
    #             #     obj.compete_score = per_score
    #             # obj.save()
    #             # tk.remove(token)
    #             # self.disconnect()
    #
    #         def disconnect(self, code=None):
    #             global x, method
    #             x -= 1
    #             print("x in dis", x)
    #             if x == 0:
    #                 method = 0
    #             self.close()
    #
    #         # def receive(self, text_data, **kwargs):
    #         #     # from_time = time.time()
    #         #     print(self.current_time)
    #         #     if self.x < 2:
    #         #         self.current_time = time.time()
    #         #     cat = self.scope["url_route"]["kwargs"]["category"]
    #         #     d = self.get_question(cat)
    #         #     time.sleep(time.time()+20-self.current_time)
    #         #     async_to_sync(self.channel_layer.group_send)(
    #         #         "player",
    #         #         {
    #         #             "type": "player.question",
    #         #             "text": json.dumps(d),
    #         #         },
    #         #     )
    #
    #         # print()
    #         # self.lt.append("1")
    #         # text_data_json = json.loads(text_data)
    #         # cat = self.scope["url_route"]["kwargs"]["category"]
    #         # token = str(text_data_json['token'])
    #         # time = int(text_data_json['time'])
    #         # self.lt.append(token)
    #         # if len(self.lt)==1:
    #         #     self.current_time = time
    #         #
    #         # d = self.get_question(cat)
    #         # # print(self.current_time+20-time.time())
    #         # time.sleep(int(self.current_time)+20-time.time())
    #         # print(self.lt)
    #         # print(self.current_time)
    #         # self.send(text_data=json.dumps({
    #         #     'message': d
    #         # }))
    #
    #         # def player_question(self, event):
    #         #     self.send(text_data=event["text"])
    #
    #     # token_obj = Token.objects.get(token=token)
    #     # print(token_obj)
    #     # user = User.objects.get(key=token_obj)
    #     # obj = CompeteScore.objects.get_or_create(user=user, category=cat_obj)
    #     # print(user.username)
    #     # if per_score>obj.compete_score:
    #     #     obj.compete_score = per_score
    #     # obj.save()
    #     # tk.remove(token)
    #     # self.disconnect()
    #
    #
    #
    # # def receive(self, text_data, **kwargs):
    # #     # from_time = time.time()
    # #     print(self.current_time)
    # #     if self.x < 2:
    # #         self.current_time = time.time()
    # #     cat = self.scope["url_route"]["kwargs"]["category"]
    # #     d = self.get_question(cat)
    # #     time.sleep(time.time()+20-self.current_time)
    # #     async_to_sync(self.channel_layer.group_send)(
    # #         "player",
    # #         {
    # #             "type": "player.question",
    # #             "text": json.dumps(d),
    # #         },
    # #     )
    #
    #
    #
    #
    #     # print()
    #     # self.lt.append("1")
    #     # text_data_json = json.loads(text_data)
    #     # cat = self.scope["url_route"]["kwargs"]["category"]
    #     # token = str(text_data_json['token'])
    #     # time = int(text_data_json['time'])
    #     # self.lt.append(token)
    #     # if len(self.lt)==1:
    #     #     self.current_time = time
    #     #
    #     # d = self.get_question(cat)
    #     # # print(self.current_time+20-time.time())
    #     # time.sleep(int(self.current_time)+20-time.time())
    #     # print(self.lt)
    #     # print(self.current_time)
    #     # self.send(text_data=json.dumps({
    #     #     'message': d
    #     # }))
    #
    # # def player_question(self, event):
    # #     self.send(text_data=event["text"])
    #
