import datetime
import json
from django.shortcuts import render
import razorpay
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from booking.tasks import send_payment_success_mail,send_booking_email,send_whatsapp_notification
from users.whatsapp import send_whatsapp_message

from packages.models import Package
from booking.constants import PaymentStatus
from .serializers import BookingSerializer, CouponAssignmentSerializer, CouponSerializer
from utilities.models import Coupon,CouponAssignment
from rest_framework.response import Response
from.models import Booking,Payment
from rest_framework import status
from django.conf import settings
from users.models import Account
from django.utils import timezone
RAZOR_ID  = settings.RAZOR_ID
RAZOR_KEY = settings.RAZOR_KEY

razorpay_client = razorpay.Client(auth=(RAZOR_ID, RAZOR_KEY))
class CouponView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        coupon_assignments = CouponAssignment.objects.filter(user=request.user)
        serializer = CouponAssignmentSerializer(coupon_assignments, many=True)
        return Response(serializer.data)

class RazorpayOrderView(APIView):
    http_method_names=('post')
    permission_classes=[IsAuthenticated]

    @staticmethod
    def post(request,*args,**kwargs):
        # try:
            user:Account=request.user
            amount = request.data['amount']
            phone_number = request.data['phone_number']
            first_name = request.data['first_name']
            last_name = request.data['last_name']
            if not user.first_name: user.first_name=first_name
            if not user.last_name: user.last_name=last_name
            if not user.phone_number:user.phone_number=phone_number
            user.save()
            razorpay_order = razorpay_client.order.create(
                {"amount": int(amount) * 100, "currency": "INR", "payment_capture": "1"}
            )


            payment  = Payment.objects.create(
                user=user,
                amount=amount,
                razorpay_order_id = razorpay_order['id'],
            )

            data  = {
                'fullName':user.full_name(),
                "merchantId": RAZOR_KEY,
                "amount": amount,
                "currency" : 'INR' ,
                "orderId" : razorpay_order["id"],
            }

            return Response(data,status=status.HTTP_202_ACCEPTED)
        # except:
        #     return Response(status=status.HTTP_401_UNAUTHORIZED)

class RazorpayCallbackView(APIView):
    http_method_names=('post')
    permission_classes=[IsAuthenticated]
    
    @staticmethod
    def post(request,*args,**kwargs):
        response = request.data['res']
        if "razorpay_signature" in response:
            data = razorpay_client.utility.verify_payment_signature(response)
            if data:

                adults = request.data.get('adults')
                children = request.data.get('children')
                infants = request.data.get('infants')
                coupon = request.data.get('coupon_id')
                package_id = request.data.get('package')
                phone_number = request.data.get('phone_number')
                start_date=datetime.datetime.strptime(request.data.get('start_date'), '%Y-%m-%dT%H:%M:%S.%fZ')
                end_date=datetime.datetime.strptime(request.data.get('end_date'), '%Y-%m-%dT%H:%M:%S.%fZ')
                package = Package.objects.get(pk=package_id)
                payment_object = Payment.objects.get(razorpay_order_id = response['razorpay_order_id'])  
                             # razorpay_payment = RazorpayPayment.objects.get(order_id=response['razorpay_order_id'])
                payment_object.status = PaymentStatus.SUCCESS
                if coupon is not None:
                    coupon_obj=CouponAssignment.objects.get(user=request.user,coupon__id=coupon)
                    coupon_obj.delete()
                payment_object.razorpay_payment_id = response['razorpay_payment_id']
                payment_object.razorpay_signature= response['razorpay_signature']          
                payment_object.save()
                
                booking_object = Booking.objects.create(
                    user = request.user,
                    payment = payment_object,
                    package=package,
                    num_adults = adults,
                    num_children = children,
                    num_infants = infants,
                    start_date=start_date.date(),
                    end_date=end_date.date(),
                    phone_number = phone_number
                )
                if coupon is not None:
                    coupon_obj=Coupon.objects.filter(id=coupon) 
                    booking_object.coupon  =coupon_obj[0]
                    booking_object.save()
                valid_coupon = Coupon.objects.filter(is_active=True, expiration_date__gte=timezone.now()).order_by('discount_price').first()
                try:
                    if coupon is None and CouponAssignment.objects.filter(user=request.user, coupon=valid_coupon).count() < 1:
                        CouponAssignment.objects.create(
                            user=request.user,
                            coupon=valid_coupon
                        )
                except:
                    pass
                email_data ={
                    'user':request.user.email,
                    'package_name':package.name,
                    'start_date':start_date,
                    'end_date':end_date
                }

                serializer = BookingSerializer(booking_object)
                booking_data  = {
                    'email':booking_object.user.email,
                    'phone_number':booking_object.phone_number,
                    'package_name':booking_object.package.name,
                    'num_adults':booking_object.num_adults,
                    'num_children':booking_object.num_children,
                    'num_infants':booking_object.num_infants,
                    'paid_amount':booking_object.payment.amount,
                    'package_main_place':booking_object.package.main_place,
                    'username':booking_object.user.full_name(),
                    'package_type':booking_object.package.type,
                    'start_date':start_date,
                    'end_date':end_date
                }
                send_payment_success_mail.delay(email_data,request.user.email)
                send_booking_email.delay(booking_data)
                send_whatsapp_notification.delay(booking_data)
                return Response( serializer.data,status=status.HTTP_200_OK)
            else:
                return Response({'status': 'Signature Mismatch!'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            error_code = response['error[code]']
            error_description = response['error[description]']
            error_source = response['error[source]']
            error_reason = response['error[reason]']
            error_metadata = json.loads(response['error[metadata]'])
            razorpay_payment =  Payment.objects.get(razorpay_order_id=error_metadata['order_id'])
            razorpay_payment.razorpay_payment_id = error_metadata['payment_id']
            razorpay_payment.razorpay_signature = "None"
            razorpay_payment.status = PaymentStatus.FAILURE
            razorpay_payment.save()

            error_status = {
                'error_code': error_code,
                'error_description': error_description,
                'error_source': error_source,
                'error_reason': error_reason,
            }

            return Response({'error_data': error_status}, status=status.HTTP_401_UNAUTHORIZED)
        
class PaymentCompletedView(APIView):
    permission_classes=[IsAuthenticated] 
    def get(self,request, *args, **kwargs):
       booking_id = request.query_params['booking']
       booking_obj = Booking.objects.select_related('coupon', 'payment', 'package').get(id=booking_id)
       if booking_obj.coupon:coupon_discount = booking_obj.coupon.discount_price 
       else: coupon_discount = 0
       data = {
           'advance_paid':booking_obj.payment.amount,
           'coupon_discount':coupon_discount,  
       }
       return Response(data,status=status.HTTP_200_OK)


