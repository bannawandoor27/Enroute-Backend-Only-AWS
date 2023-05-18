from rest_framework.generics import RetrieveAPIView,ListAPIView
from .serializers import ExperienceSerializer,AllExperienceSerializer,CommentSerializer
from .models import Experience,Comment

class ExperienceDetailView(RetrieveAPIView):
    serializer_class = ExperienceSerializer
    def get_queryset(self):
        queryset = Experience.objects.prefetch_related('paragraphs', 'tags')
        return queryset

class ExperianceView(ListAPIView):
    queryset = Experience.objects.all().order_by('?')
    serializer_class = AllExperienceSerializer

class CommentsView(ListAPIView):
    serializer_class = CommentSerializer
    def get_queryset(self):
        id=self.request.query_params['id']
        queryset=Comment.objects.filter(experiance__pk=id)
        print(queryset)
        return queryset

