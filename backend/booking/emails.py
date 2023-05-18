from django.core.mail import EmailMessage
from django.template.loader import get_template
from django.conf import settings

def payment_success_mail(data,mail):
    subject = 'Booking Successfull'
    html_content = get_template('confirm_email.html').render(data)
    from_email = settings.EMAIL_HOST_USER
    message = EmailMessage(subject,html_content,from_email,[mail])
    message.content_subtype='html'
    message.send()

def booking_cancelled_mail(data,mail):
    subject = 'Booking Cancelled'
    html_content = get_template('cancel_email.html').render(data)
    from_email = settings.EMAIL_HOST_USER
    message = EmailMessage(subject,html_content,from_email,[mail])
    message.content_subtype='html'
    message.send()