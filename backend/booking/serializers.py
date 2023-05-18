from rest_framework import serializers
from booking.models import Booking, Payment
from packages.models import Package
from utilities.models import Coupon, CouponAssignment
from users.models import Account
class CouponSerializer(serializers.ModelSerializer):
    is_valid = serializers.BooleanField(read_only=True)
    class Meta:
        model = Coupon
        fields = '__all__'
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['is_valid'] = instance.is_valid()
        return data
class CouponAssignmentSerializer(serializers.ModelSerializer):
    coupon = CouponSerializer()

    class Meta:
        model = CouponAssignment
        fields = ('coupon', 'assigned_at',)
class BookingSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=Account.objects.all())
    package = serializers.PrimaryKeyRelatedField(queryset=Package.objects.all())
    payment = serializers.PrimaryKeyRelatedField(queryset=Payment.objects.all())
    coupon = serializers.PrimaryKeyRelatedField(queryset=Coupon.objects.all(), required=False)

    class Meta:
        model = Booking
        fields = ('id', 'user', 'package', 'date_booked', 'start_date', 'end_date',
                  'num_adults', 'num_infants', 'num_children', 'phone_number', 'payment','coupon','booking_code','status')
