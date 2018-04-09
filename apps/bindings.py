from channels_framework.bindings import ResourceBinding

from .models import CompeteQuiz
# from .serializers import QuestionSerializer


class QuestionBinding(ResourceBinding):

    model = CompeteQuiz
    stream = "questions"
    # serializer_class = QuestionSerializer
    queryset = CompeteQuiz.objects.all()
