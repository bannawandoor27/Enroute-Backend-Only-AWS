from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status,permissions
from rest_framework.response import Response
from booking.tasks import booking_cancelled_mail_async, send_mail_async, send_otp,send_whatsapp_message_async
from booking.constants import BookingStatus  
from .serializers import *
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from .models import Account
from .emails import *
from rest_framework.decorators import api_view,permission_classes
from django.contrib.sites.shortcuts import get_current_site
from django.conf import settings
import requests,jwt,datetime
from rest_framework.exceptions import AuthenticationFailed 
import pyotp
from rest_framework.pagination import PageNumberPagination
from rest_framework import viewsets
from booking.models import Booking
from rest_framework.generics import ListCreateAPIView
class generateKey:
    @staticmethod
    def returnValue():
        secret = pyotp.random_base32()        
        totp = pyotp.TOTP(secret, interval=86400)
        OTP = totp.now()
        return {"totp":secret,"OTP":OTP}
class CreateAccount(APIView):
   permission_classes=[permissions.AllowAny]
   def post(self,request):
       reg_serializer=RegistrationSerializer(data=request.data)
       try:
            if reg_serializer.is_valid(raise_exception=True):
                new_user=reg_serializer.save()
                new_user.is_active=False
                new_user.save()
                if new_user:
                    send_otp.delay(reg_serializer.data['email'])
                    return Response(status=status.HTTP_201_CREATED)
       except ValidationError as e:
            if e.get_codes()['email']==['unique']:
                user = Account.objects.get(email=reg_serializer.data['email'])
                if user.otp and user.is_verified == False :
                    print(reg_serializer.errors)
                    return Response({'email':'Verify your OTP to proceed'},status=status.HTTP_401_UNAUTHORIZED)
            return Response(reg_serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class VerifyOTP(APIView):
    def post(self, request, *args, **kwargs):        
        try:
            data = request.data
            serializer = VerifyAccountSerializer(data=data)
            if serializer.is_valid():

                email = serializer.data['email']

                otp = serializer.data['otp']
                user = Account.objects.get(email=email)
                if not user:
                    return Response({'error':'Invalid Email Address'},status=status.HTTP_400_BAD_REQUEST)
                if not user.otp==otp:
                    return Response({'error':'Invalid OTP'},status=status.HTTP_406_NOT_ACCEPTABLE)
                user.is_verified = True
             
                user.otp = None
                user.is_active = True
                user.save()
                r=requests.post(f'http://{get_current_site(request)}/api/users/auth/token/', data = {
                'username':serializer.data['email'],
                'password':serializer.data['password'],
                'client_id':settings.AUTH_CLIENT_ID,
                'client_secret':settings.AUTH_CLIENT_SECRET,
                'grant_type':'password'
                 })
                print(r.json())
                return Response(r.json(),status=status.HTTP_202_ACCEPTED)
                
            return Response({'error': 'invalid Data'},status=status.HTTP_400_BAD_REQUEST)
    
        except:
            return Response({'error':'Something went wrong!'},status=status.HTTP_401_UNAUTHORIZED)       
        

class ForgotPass(APIView):
    def post(self, request):
        data = request.data
        print(data)
        pass_serialzer = ForgotPassSerializer(data=data)
        print(pass_serialzer)
        if pass_serialzer.is_valid():
            email = pass_serialzer.data['email']
            try:
                user_obj = Account.objects.get(email=email)
            except Account.DoesNotExist:
                return Response(data={'error':'No Account with this email'},status=status.HTTP_404_NOT_FOUND)
            subject = f'Forgot Password verification mail'
            try:
                send_otp.delay(email,subject='Forgot Password Verification')
                return Response(status=status.HTTP_202_ACCEPTED)
            except:
                return Response(data={'error':'Email sending failed'},status=status.HTTP_401_UNAUTHORIZED)
        return Response(data={'error':'Invalid Email'},status=status.HTTP_400_BAD_REQUEST)

class ForgotPassOtp(APIView):
    
    def post(self, request, *args, **kwargs):
        otp_serializer = ForgotPassOtpSerializer(data=request.data)
        if otp_serializer.is_valid():
            email = otp_serializer.data['email']
            otp  = otp_serializer.data['otp']
            try:
                user =  Account.objects.get(email=email,otp=otp)
                user.otp = None
                payload = {
                        'user_id': user.id,
                        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=30),
                            }
                token = jwt.encode(payload,'secret_key', algorithm='HS256')
                return Response(data={'success': 'OTP valid','token':token},status=status.HTTP_202_ACCEPTED)
            except: return Response(data={'error': 'Invalid otp'},status=status.HTTP_400_BAD_REQUEST)
        return Response(data={'error': 'verification failed'},status=status.HTTP_403_FORBIDDEN)
    
class ForgotChangePassView(APIView):
    def post(self, request, *args, **kwargs):
        change_pass_serializer = ForgotChangePassSerializer(data=request.data)
        print(request.data)
        if change_pass_serializer.is_valid():
            password = change_pass_serializer.data['password']
            token = change_pass_serializer.data['token']
            try:
                payload = jwt.decode(token,'secret_key', algorithms=['HS256'])
            except jwt.DecodeError:
                return Response({'error':'Decode error'},status=status.HTTP_401_UNAUTHORIZED)
            except jwt.ExpiredSignatureError:
                raise AuthenticationFailed('Invalid token')
            try:
                user_id = payload['user_id']
                user = Account.objects.get(id=user_id)
                user.set_password(password)
                user.save()
                r=requests.post(f'http://{get_current_site(request)}/api/users/auth/token/', data = {
                'username':user.email,
                'password':password,
                'client_id':settings.AUTH_CLIENT_ID,
                'client_secret':settings.AUTH_CLIENT_SECRET,
                'grant_type':'password'
                 })
                print(r.json())
                return Response(data=r.json(),status=status.HTTP_200_OK)
            except:
                return Response(status=status.HTTP_403_FORBIDDEN)
                    
        return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def user_detail(request):
    user = request.user
    if not user.is_verified and user.otp:
        return Response(status=status.HTTP_403_FORBIDDEN)
    if request.method == 'GET':
        serializer = UserSerializer(user,context={'request': request})
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = UserSerializer(user, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
           
            serializer.save()
            print(serializer.data)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class BookingListAPIView(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = BookingSerializer
    pagination_class= PageNumberPagination
    pagination_class.page_size=4
    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user).prefetch_related('package', 'payment', 'coupon').order_by('-date_booked')

class BookingCancel(APIView):
    permission_classes=[IsAuthenticated]
    def patch(self, request,id):
        try:
            booking = Booking.objects.get(user=request.user,id=id)
            booking.status=BookingStatus.CANCELLED
            mail = booking.user.email
            data = {
                'user':booking.user.email,
                'package_name':booking.package.name
            }
            booking_cancelled_mail_async.delay(data=data,mail=mail)

            send_mail_async.delay(
                    subject='Booking cancelled On Enroute Travel',
                    message=f'''
                    Client mail : {booking.user.email}
                    Client phone : {booking.phone_number}
                    Package  :{booking.package.name} , {booking.package.main_place}
                    Scheduled Date: {booking.start_date}
                    Amount paid : {booking.payment.amount}
                    Client name : {booking.user.full_name()}
                    ''',
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=['hasanul1908350@st.jmi.ac.in']
                )
            send_whatsapp_message_async.delay(
              message=  f'''
                    *Booking Cancelled*

                    Important!! ⚠️⚠️⚠️
                   *Client Cancelled package on Enroute Travel!*

                    Client mail : {booking.user.email}
                    Client phone : {booking.phone_number}
                    Package  :{booking.package.name} , {booking.package.main_place}
                    Scheduled Date: {booking.start_date}
                    Amount paid : {booking.payment.amount}
                    Client name : {booking.user.full_name()}
                    ''',
                    number=settings.WHATSAPP_NUM
            )
            booking.save()
            return Response(status=status.HTTP_202_ACCEPTED)
        except:
            return Response(status=status.HTTP_403_FORBIDDEN)

