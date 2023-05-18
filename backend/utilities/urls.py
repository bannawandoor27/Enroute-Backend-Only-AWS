from django.urls import path
from .views import ContactView, EnquiryView,Testimonials

testimonials = Testimonials.as_view()

urlpatterns = [
  path('enquiry/',EnquiryView.as_view(),name='enquiry'),  
  path('testimonials/',testimonials,name='testimonials'), 
  path('contactUs/',ContactView.as_view(),name='contacts'),
]