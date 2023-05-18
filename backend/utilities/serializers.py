from rest_framework import serializers
from .models import Contact, Enquiry, Testimonial



class EnquirySerializer(serializers.ModelSerializer):
    class Meta:
        model=Enquiry
        fields = '__all__'

class TestimonialSerializer(serializers.ModelSerializer):
    class Meta:
        model=Testimonial
        fields = '__all__'


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ['id', 'name', 'email', 'message']