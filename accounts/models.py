from django.db import models
from django.contrib.auth.models import User
from django.core.validators import *
from django.core import validators

# Create your models here.
class Wishlist(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    created_date=models.DateTimeField(auto_now_add=True)

class Bookings(models.Model):
    PAYMENT=(
        ('Cash on Delivery', 'Cash on delivery'),
        ('Esewa','Esewa') #one for user, one for database
    )
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    total_price=models.IntegerField()
    payment_method=models.CharField(max_length=100,choices=PAYMENT)
    payment_status=models.BooleanField(default=False,null=True)
    contact_no=models.CharField(validators=[MinLengthValidator(9),MaxLengthValidator(10)], max_length=10)
    address=models.CharField(max_length=200)
    created_date=models.DateTimeField(auto_now_add=True)

