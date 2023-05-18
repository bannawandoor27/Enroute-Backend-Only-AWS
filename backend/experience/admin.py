from django.contrib import admin
from .models import Experience, Paragraph, Tags, Comment

class ParagraphInline(admin.TabularInline):
    model = Paragraph
    extra = 5

class TagsInline(admin.TabularInline):
    model = Tags
    extra = 5

class CommentInline(admin.TabularInline):
    model = Comment
    extra = 1

@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ('id', 'experience_header', 'traveler_name', 'designation', 'date_published')
    search_fields = ('id', 'experience_header', 'traveler_name', 'designation')
    inlines = [ParagraphInline, TagsInline, CommentInline]
    ordering = ('-id',)
@admin.register(Paragraph)
class ParagraphAdmin(admin.ModelAdmin):
    list_display = ('id', 'experience', 'paragraph_number', 'header', 'created_at')
    list_filter = ('experience',)
    search_fields = ('id', 'experience__experience_header', 'paragraph_number', 'header')
    ordering=('-created_at',)
@admin.register(Tags)
class TagsAdmin(admin.ModelAdmin):
    list_display = ('id', 'experience', 'tag')
    list_filter = ('experience',)
    search_fields = ('id', 'experience__experience_header', 'tag')
    ordering=('id',)
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'experiance', 'user', 'comment_text', 'posted_at')
    list_filter = ('experiance', 'user')
    search_fields = ('id', 'experiance__experience_header', 'user__email', 'comment_text')
    ordering=('id',)