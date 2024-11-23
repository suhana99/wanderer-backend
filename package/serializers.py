from rest_framework import serializers
from .models import Package,Review

class PackageSerializer(serializers.ModelSerializer):
    image=serializers.ImageField()

    class Meta:
        model = Package
        fields = ['id','image', 'name', 'description', 'price', 'location', 'duration','availability']


class ReviewSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'username', 'rating', 'comment', 'date_added']

