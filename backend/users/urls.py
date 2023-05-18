from django.urls import path,include
from .views import CreateAccount,VerifyOTP,ForgotPass,ForgotPassOtp,ForgotChangePassView,user_detail,BookingListAPIView,BookingCancel

urlpatterns = [
    path('auth/', include('rest_framework.urls')),
    path('auth/', include('drf_social_oauth2.urls',namespace='drf')),
    path('register/',CreateAccount.as_view(),name='register'),
    path('verify/',VerifyOTP.as_view(),name='otp_verify'),
    path('forgot_pass',ForgotPass.as_view(),name='forgot_pass'),
    path('forgot_pass_otp',ForgotPassOtp.as_view(),name='forgot_pass'),
    path('forgot_change_password',ForgotChangePassView.as_view()),
    path('user_profile/',user_detail),
    path('booking_detail/',BookingListAPIView.as_view()),
    path('booking_cancel/<int:id>',BookingCancel.as_view()),

]

