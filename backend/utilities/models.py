from django.db import models
from django.utils import timezone
from users.models import Account
# Create your models here.
import datetime
class Enquiry(models.Model):
    client_name = models.CharField(max_length=50,blank=False)
    client_phone = models.CharField(blank=False,max_length=12)
    client_message = models.TextField(editable=True,blank=True)
    checked = models.BooleanField(default=False)

    def client_request(self):
        return f'''
            *Enquiry*

            Hi Admin, New enquiry recieved from enroutetravel.co.in
            -> Client Name : {self.client_name}
            -> Client Phone : {self.client_phone}
            -> Client Message :{self.client_message if self.client_message else ''}
             
            Date : {datetime.date.today()}
        '''
    def __str__(self) -> str:
        return self.client_name

class Testimonial(models.Model):
    client_name = models.CharField(max_length=255,blank=False)
    client_place = models.CharField(max_length=255)
    client_image = models.ImageField(upload_to='testimonials')
    content  = models.TextField()

    def __str__(self):
        return self.client_name

class Contact(models.Model):
    name = models.CharField(max_length=255,blank=False)
    email = models.CharField(max_length=255)
    message = models.TextField()
    def __str__(self):
        return self.name
    
class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True) 
    coupon_name = models.CharField(max_length=255,default='Enroute Special')
    is_active = models.BooleanField(default=True)
    discount_price = models.IntegerField() 
    expiration_date = models.DateTimeField() 

    def is_valid(self):
        return self.is_active and timezone.now() <= self.expiration_date
    def __str__(self):
        return self.coupon_name

class CouponAssignment(models.Model):
    coupon = models.ForeignKey(Coupon, on_delete=models.CASCADE)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    assigned_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f'{self.coupon.coupon_name} {self.user.email}'