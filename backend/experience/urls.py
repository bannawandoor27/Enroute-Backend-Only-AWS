from django.urls import path
from .views import ExperienceDetailView,ExperianceView,CommentsView
urlpatterns = [
       path('experience_detail/<int:pk>/', ExperienceDetailView.as_view()),
       path('all_experiences/',ExperianceView.as_view()),
       path('experience_comments/',CommentsView.as_view() )

]