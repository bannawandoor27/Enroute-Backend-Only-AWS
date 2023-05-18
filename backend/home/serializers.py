from rest_framework import serializers

from .models import Video

class VideoSerializer(serializers.ModelSerializer):
    thumbnail_url = serializers.SerializerMethodField()

    class Meta:
        model = Video
        fields = ('id', 'title', 'link', 'thumbnail_url')
    def get_thumbnail_url(self, obj):
        if obj.thumbnail:
            return self.context['request'].build_absolute_uri(obj.thumbnail.url)
        return None
    
class FavoriteDestinationSerializer(serializers.Serializer):
    main_place = serializers.CharField()
    package_count = serializers.IntegerField()
    image_url = serializers.URLField()

    class Meta:
        fields = ('main_place', 'package_count', 'image_url')

class CategoryPackageSerializer(serializers.Serializer):
    category = serializers.CharField()
    package_count = serializers.IntegerField()
    image_url = serializers.URLField()

    class Meta:
        fields = ('category', 'package_count', 'image_url')
