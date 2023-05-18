import uuid
from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from utilities.models import Coupon
from packages.models import Package
from .constants import PaymentStatus,BookingStatus
from django.utils.translation import gettext_lazy as _


User = get_user_model()
class Payment(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    razorpay_payment_id = models.CharField( _("Payment ID"), max_length=36, null=False, blank=False)
    razorpay_order_id = models.CharField( _("Order ID"), max_length=40, null=False, blank=False)
    razorpay_signature = models.CharField(_("Signature ID"), max_length=128, null=False, blank=False)
    amount = models.FloatField()
    status = models.CharField(
        _("Payment Status"),
        default=PaymentStatus.PENDING,
        max_length=254,
        blank=False,
        null=False,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.full_name()} booked'
    
    
class Booking(models.Model):
    booking_code = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    package = models.ForeignKey(Package, on_delete=models.CASCADE)
    date_booked = models.DateTimeField(default=timezone.now)
    start_date = models.DateField(blank=False)
    end_date = models.DateField(blank=False)
    num_adults = models.PositiveIntegerField(blank=False,null=False)
    num_infants = models.PositiveIntegerField(blank=True,null=True,default=0)
    num_children = models.PositiveIntegerField(blank=True,null=True,default=0,)
    phone_number  =models.CharField(max_length=10,blank=True)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, null=True, blank=True)
    coupon  = models.ForeignKey(Coupon, on_delete=models.SET_NULL, null=True, blank=True)
    status= models.CharField(
        _("Booking Status"),
        default=BookingStatus.SUCCESS,
        max_length=254,
        blank=False,
        null=False,
    )

    def save(self, *args, **kwargs):
        if not self.booking_code:
            self.booking_code = str(uuid.uuid4())
            while Booking.objects.filter(booking_code=self.booking_code).exists():
                self.booking_code = str(uuid.uuid4())
        super().save(*args, **kwargs)

    def __str__(self):
        return f'"{self.user.email}" booked "{self.package.name}" on "{str(self.date_booked)[:10]}"'

