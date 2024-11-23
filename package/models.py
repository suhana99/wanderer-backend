from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.conf import settings
from users.models import CustomUser
# Create your models here.

class PackageManager(models.Manager):
    def count_unavailable(self):
        return self.filter(availability=False).count()

class Package(models.Model):
    name=models.CharField(max_length=100)
    image=models.ImageField(upload_to='uploads')
    description=models.CharField(max_length=200)
    price=models.FloatField()
    location=models.CharField(max_length=100)
    duration=models.IntegerField()
    availability=models.BooleanField()
    created_at=models.DateTimeField(auto_now_add=True)
    objects = PackageManager()
    def __str__(self):
        return self.name
    
    
class Review(models.Model):
    package = models.ForeignKey(Package, related_name='reviews', on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    rating=models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    comment=models.TextField()
    date_added=models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.user.username