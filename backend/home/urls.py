from django.urls import path
from .views import *
from utilities.urls import testimonials

urlpatterns = [
    path('favorites/',home,name='favorites'),
    path('featured/',home,name='featured'),
    path('category/',home,name='category'),
    path('videos/',home,name='videos'),
    path('testimonials/',testimonials,name='testimonials'), 
    

]