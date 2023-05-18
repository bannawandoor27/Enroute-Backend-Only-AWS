from django.core.mail import send_mail
from django.conf import settings

def send_enquiry(message):
    subject = 'New Enquiry From Website'
    email_from = settings.EMAIL_HOST
    # email = ['booking@enroutetravel.co.in','getenroutetravel@gmail.com']
    email = ['hasanulbannac@outlook.com']
    send_mail(subject,message,email_from,email)