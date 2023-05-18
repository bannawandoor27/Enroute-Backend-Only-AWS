from django.db import models

class Video(models.Model):
    title = models.CharField(max_length=100)
    link = models.URLField()
    thumbnail = models.ImageField(upload_to='thumbnails/')
    def __str__(self):
        return self.title