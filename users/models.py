from django.db import models
from django.contrib.auth.models import AbstractUser
from rest_framework_simplejwt.tokens import RefreshToken

# Create your models here.
class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('user', 'User'),
        ('admin', 'Admin'),
        ('hotel_owner', 'Hotel Owner'),
        ('activity_lister', 'Activity Lister'),
    ]
    STATUS=[
        ('approved','Approved'),
        ('rejected','Rejected'),
        ('pending','Pending')
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='admin')
    is_seller=models.BooleanField(default=False)
    email = models.EmailField(unique=True,null=False)
    is_approved=models.CharField(max_length=20,choices=STATUS,default='pending')
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


    def __str__(self):
        return self.username
    
    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
    
    