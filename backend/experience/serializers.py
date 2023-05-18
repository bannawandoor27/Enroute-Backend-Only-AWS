from django.conf import settings
from rest_framework import serializers
from .models import Experience, Paragraph, Tags,Comment

class ParagraphSerializer(serializers.ModelSerializer):
    class Meta:
        model = Paragraph
        fields = ('paragraph_number', 'header', 'description', 'created_at')

class TagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tags
        fields = ('tag',)

class ExperienceSerializer(serializers.ModelSerializer):
    paragraphs = ParagraphSerializer(many=True)
    tags = TagsSerializer(many=True)

    class Meta:
        model = Experience
        fields = ('traveler_name', 'traveler_image', 'designation', 'experience_header', 'experience_sub_header', 'experience_main_image',
                   'experience_sub_image', 'date_published', 'paragraphs', 'tags','traveler_description')

class AllExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model=Experience
        fields  =('id','traveler_name','traveler_image','date_published','experience_header', 'experience_sub_header','experience_main_image')

class CommentSerializer(serializers.ModelSerializer):
    user  = serializers.SerializerMethodField()
    def get_user(self, obj):
        user = obj.user
        return {

            'username': user.first_name+' '+user.last_name,
            'email': user.email,
            'profile_image': f'{settings.API_BASE_URL}{user.profile_image}'
        }
    class Meta:
        model=Comment
        fields = ('id','user','posted_at','comment_text')
        