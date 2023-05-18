from django.db import models
from django.contrib.postgres.fields import ArrayField
# from django.contrib.gis.db import models as locationModels
from django.db.models import Avg
from users.models import Account
from django.core.validators import MaxValueValidator
import datetime



class Package(models.Model):
    name = models.CharField(max_length=255,blank=False)
    category = models.CharField(max_length=255)
    main_place = models.CharField(max_length=255,default='Kashmir')
    places = ArrayField(models.CharField(max_length=255), blank=False)
    duration = models.CharField(max_length=255, blank=False)
    inclusions = ArrayField(models.TextField())
    exclusions = ArrayField(models.TextField())
    location = models.TextField(blank=True,null=True)
    average_rating = models.FloatField(null=True, blank=True)
    total_reviews = models.IntegerField(null=True, blank=True)
    price = models.IntegerField(default=20000)
    itinerary_pdf = models.FileField(upload_to='itinerary/',blank=True,null=True)
    discount_percent = models.PositiveIntegerField(default=0)
    type = models.CharField(max_length = 255, null=True, blank=True,default='Deluxe')
    is_active = models.BooleanField(default=True,blank=False)
    

    def update_review_stats(self):
        reviews = self.reviews.all()
        self.average_rating = reviews.aggregate(Avg('rating'))['rating__avg']
        self.total_reviews = reviews.count()
        self.save()
    def discount_price(self):
        return round((self.price/100)*(100-self.discount_percent),2)
    def __str__(self) -> str:
        return self.name
class Itinerary(models.Model):
    package = models.ForeignKey(Package,on_delete=models.CASCADE,related_name='itinerary',default='')
    day  = models.IntegerField()
    activity = models.TextField()

    def __str__(self):
        return f'{self.package} , Day {self.day}'

class PackageImage(models.Model):
    package = models.ForeignKey(Package,on_delete=models.CASCADE,related_name='images')
    image = models.ImageField(upload_to='images/')
    def __str__(self):
        return self.package.name
class Review(models.Model):
    user = models.ForeignKey(Account,on_delete=models.CASCADE)
    package = models.ForeignKey(Package, on_delete=models.CASCADE, related_name='reviews')
    review_text = models.TextField()
    rating = models.PositiveIntegerField(validators=[MaxValueValidator(5)])
    created_at = models.DateField(auto_now=True)

    def __str__(self):
        return f'{self.user}  on {self.package.name}'


class Wishlist(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    packages = models.ManyToManyField(Package)
    added_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.user.full_name()





