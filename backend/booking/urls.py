from django.urls import path
from .views import *

urlpatterns = [
   path('coupons/',CouponView.as_view()) ,
   path('razorpay_booking/',RazorpayOrderView.as_view()),
   path('razorpay_callback/',RazorpayCallbackView.as_view()),
   path('payment_completed/',PaymentCompletedView.as_view())
]