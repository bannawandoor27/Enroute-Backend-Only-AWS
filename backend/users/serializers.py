from django.db import IntegrityError
from rest_framework import serializers
from utilities.models import Coupon
from packages.models import Package

from booking.models import Payment

from booking.models import Booking
from .models import Account

class RegistrationSerializer(serializers.ModelSerializer):
   class Meta:
       model=Account
       fields='__all__'
       extra_kwargs={'password':{'write_only':True}}
   def create(self,validated_data):
       password=validated_data.pop('password',None)
       
       try:
            instance=self.Meta.model(**validated_data)
            print(instance)
       except IntegrityError as e:
           if 'Acccount with this email already exists' in str(e):
               
               raise serializers.ValidationError({'email': 'An Enroute user with this email already exists.'})
       if password is not None:
           instance.set_password(password)
       instance.save()
       return instance
   
class VerifyAccountSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp  = serializers.IntegerField()
    password = serializers.CharField()

class ForgotPassSerializer(serializers.Serializer):
    email = serializers.EmailField()

class ForgotPassOtpSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp  = serializers.IntegerField()

class ForgotChangePassSerializer(serializers.Serializer):
    password = serializers.CharField()
    token = serializers.CharField()

class UserSerializer(serializers.ModelSerializer):
    profile_image_url = serializers.SerializerMethodField()
    profile_image = serializers.ImageField(required=True, write_only=True)

    class Meta:
        model = Account
        fields =('email','first_name','last_name','gender','address','phone_number','profile_image_url','profile_image')
        read_only_fields = ('email',) 

    def get_profile_image_url(self, obj):
        request = self.context.get('request')
        if obj.profile_image and request:
            return request.build_absolute_uri(obj.profile_image.url)
        return None
    


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['amount','status']

class PackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Package
        fields = ['category','duration','name','main_place','type','id','price','discount_price']

class CouponSerializer(serializers.ModelSerializer):
    class Meta:
        model=Coupon
        fields=['discount_price']

        
class BookingSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    package= PackageSerializer()
    payment = PaymentSerializer()
    coupon  =CouponSerializer()
    class Meta:
        model = Booking
        fields = '__all__'