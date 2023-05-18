import random
from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from utilities.emails import send_enquiry
from booking.emails import payment_success_mail,booking_cancelled_mail
from users.whatsapp import send_whatsapp_message
from users.models import Account

@shared_task
def send_booking_email(booking_object):
    send_mail(
        subject='🟢🟢New Booking On Enroute Travel',
        message=f'''
        client mail : {booking_object['email']}
        client phone : {booking_object['phone_number']}
        package  :{booking_object['package_name']} , {booking_object['package_main_place']}
        category :{booking_object['package_type']}
        date : {booking_object['start_date']}
        amount paid : {booking_object['paid_amount']}
        client name : {booking_object['username']}
        guests : {booking_object['num_adults']} adults , {booking_object['num_children'] } children, {booking_object['num_infants']} infants
        ''',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=['hasanul1908350@st.jmi.ac.in']
    )

@shared_task
def send_whatsapp_notification(booking_object):
    send_whatsapp_message(
        f'''
        *Booking*

        *New booking for {booking_object['package_main_place']}*
        
        client mail : {booking_object['email']}
        client phone : {booking_object['phone_number']}
        package  :{booking_object['package_name']} , {booking_object['package_main_place']}
        category :{booking_object['package_type']}
        date : {booking_object['start_date']}
        amount paid : {booking_object['paid_amount']}
        client name : {booking_object['username']}
        guests : {booking_object['num_adults']} adults , {booking_object['num_children'] } children, {booking_object['num_infants']} infants
        ''',
        number=settings.WHATSAPP_NUM
    )

@shared_task
def send_payment_success_mail(email_data, user_email):
    payment_success_mail(email_data, user_email)

@shared_task
def send_mail_async(subject, message,from_email,recipient_list):
    send_mail(subject, message,from_email,recipient_list)

@shared_task
def booking_cancelled_mail_async(data,mail):
    booking_cancelled_mail(data,mail)

@shared_task
def send_whatsapp_message_async(message, number):
    send_whatsapp_message(message, number)

@shared_task
def send_enquiry_async(message):
    send_enquiry(message)

@shared_task
def send_otp(email,subject=f'OTP for activating your Enroute account'):
    otp = random.randint(100000,999999)
    message = f'Greetings from Enroute! Your otp for activation is {otp}. Kindly avoid this message if its not you'
    email_from = settings.EMAIL_HOST
    send_mail(subject,message,email_from,[email])
    user_obj = Account.objects.get(email=email)
    user_obj.otp = otp
    user_obj.save()