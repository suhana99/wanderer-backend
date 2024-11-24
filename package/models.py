from django.db import models
from django.conf import settings
from django.utils import timezone
from users.models import CustomUser

# Hotel Model
class Hotel(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # Refers to the CustomUser model
        on_delete=models.CASCADE,
        related_name='hotels',
        limit_choices_to={'role': 'hotel_owner'},  # Restrict to hotel owners
    )
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    availability = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} - {self.location}"


# Activity Model
class Activity(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='activities',
        limit_choices_to={'role': 'activity_lister'},  # Restrict to activity listers
    )
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    availability = models.BooleanField(default=True)

    def __str__(self):
        return f"Activity: {self.name} at {self.location}"


class PackageManager(models.Manager):
    def count_unavailable(self):
        return self.filter(availability=False).count()
    
# Updated Package Model
class Package(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='uploads')
    description = models.TextField()
    price = models.FloatField()
    location = models.CharField(max_length=100)
    duration = models.IntegerField()  # Duration in days
    availability = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    objects = PackageManager()

    # Many-to-Many relationships
    hotels = models.ManyToManyField(
        Hotel,
        related_name='packages',
        blank=True
    )
    activities = models.ManyToManyField(
        Activity,
        related_name='packages',
        blank=True
    )

    def __str__(self):
        return f"Package: {self.name}, Location: {self.location}"



# Review Model
class Review(models.Model):
    package = models.ForeignKey(Package, related_name='reviews', on_delete=models.CASCADE)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    comment = models.TextField()
    date_added = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Review by {self.user.email} for {self.package.name}"
