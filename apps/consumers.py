# from channels.generic.websockets import WebsocketDemultiplexer, JsonWebsocketConsumer
# from .models import CompeteQuiz
# from django.http import Http404
#
#
# class CompeteQuizHere(JsonWebsocketConsumer):
#
#     def connect(self, message, multiplexer, **kwargs):
#         multiplexer.send({"status": "You have been connected to emergency portal"})
#
#     def receive(self, content, multiplexer, **kwargs):
#         print(content)
#
#     def disconnect(self, message, multiplexer, **kwargs):
#         print("Stream %s is closed" % multiplexer.stream)
#
#
# class Demultiplexer(WebsocketDemultiplexer):
#
#     consumers = {
#         "compete": CompeteQuizHere,
#     }
#
