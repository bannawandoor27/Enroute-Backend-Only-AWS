from django.db import models
from users.models import Account
# Create your models here.

class Experience(models.Model):
    traveler_name = models.CharField(max_length=255)
    traveler_image = models.ImageField(blank=True, null=True,upload_to='experience/traveler_image/')
    traveler_description = models.TextField(blank=True,null=True,default=' is an avid traveler who loves to explore new places, learn about different cultures, and meet new people.')
    designation = models.CharField(max_length=255)
    experience_header = models.TextField(blank=False, null=False)
    experience_sub_header = models.TextField(blank=False, null=False)
    experience_main_image = models.ImageField(blank=False, null=False,upload_to='experience/experience_image')
    experience_sub_image = models.ImageField(blank=True, null=True, upload_to='experience/experience_image/')
    date_published = models.DateField(auto_now=True)
    def __str__(self):
        return self.experience_header

class Paragraph(models.Model):
    paragraph_number = models.PositiveIntegerField(null=False,blank=False)
    experience = models.ForeignKey(Experience,on_delete=models.CASCADE,related_name='paragraphs')
    header = models.TextField(blank=True,null=True)
    description = models.TextField(blank=False,null=False)
    created_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f'{self.paragraph_number} . {self.experience.experience_header}'

class Tags(models.Model):
    experience = models.ForeignKey(Experience,on_delete=models.CASCADE,related_name='tags')
    tag = models.CharField(max_length=255)
    def __str__(self):
        return self.tag

class Comment(models.Model):
    experiance = models.ForeignKey(Experience, on_delete=models.CASCADE,related_name='comments',)
    user = models.ForeignKey(Account, on_delete=models.CASCADE) 
    comment_text = models.TextField(max_length=700)
    posted_at = models.DateField(auto_now=True)
    def __str__(self):
        return f' |{self.user.full_name()}| on |{self.experiance.experience_header}|'