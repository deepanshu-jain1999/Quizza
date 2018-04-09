from channels.routing import route_class, route
from apps.bindings import QuestionBinding
from channels.generic.websockets import WebsocketDemultiplexer


class APIDemultiplexer(WebsocketDemultiplexer):
    mapping = {
      'question': 'questions_channel'
    }


channel_routing = [
  route_class(APIDemultiplexer),
  route("question_channel", QuestionBinding.consumer)
]