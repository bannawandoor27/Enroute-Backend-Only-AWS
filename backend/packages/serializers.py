from rest_framework import serializers
from django.conf import settings
from booking.models import Booking
from users.models import Account
from .models import Itinerary, Package, PackageImage,Review, Wishlist
class ItinerarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Itinerary
        fields = ( 'day', 'activity')

class PackageImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PackageImage
        fields = ('id', 'package', 'image')

class ReviewSerializer(serializers.ModelSerializer):
    user  = serializers.SerializerMethodField()
    has_booked = serializers.SerializerMethodField()
    def get_user(self, obj):
        user = obj.user
        return {

            'username': user.first_name+' '+user.last_name,
            'email': user.email,
            'profile_image': f'{settings.API_BASE_URL}{user.profile_image}'
        }
    def get_has_booked(self, obj):
            user = obj.user
            package = obj.package
            has_booked = Booking.objects.filter(user=user, package=package).exists()
            return has_booked

    class Meta:
        model = Review
        fields = ('id', 'user', 'package', 'review_text', 'rating','created_at','has_booked')

class PackageImageSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    class Meta:
        model = PackageImage
        fields = '__all__'

    def get_image_url(self, obj):
        request = self.context.get('request')
        absolute_url = request.build_absolute_uri(obj.image.url)
        absolute_url = absolute_url.replace('http://', 'https://')
        return absolute_url

class PackageSerializer(serializers.ModelSerializer):
    images = PackageImageSerializer(many=True,read_only=True,)
    itinerary = ItinerarySerializer(many=True, read_only=True)
    reviews = ReviewSerializer(many=True, read_only=True)
    class Meta:
        model = Package
        fields = ('id', 'name', 'category', 'main_place', 'places', 'duration',
                  'inclusions', 'exclusions', 'average_rating', 'total_reviews', 'images',
                  'discount_percent','price','type','itinerary', 'reviews',
                  'location','is_active','discount_price','itinerary_pdf')
        prefetch_related = ('images', )

class WishlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wishlist
        fields = ('id', 'user', 'packages', 'added_at', 'is_active')
        
    user = serializers.PrimaryKeyRelatedField(queryset=Account.objects.all())
    packages = serializers.PrimaryKeyRelatedField(queryset=Package.objects.all(), many=True)