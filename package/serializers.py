from rest_framework import serializers
from .models import *


class HotelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hotel
        fields = ['id', 'name', 'location', 'availability']

class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = ['id', 'name', 'location', 'availability']

class PackageSerializer(serializers.ModelSerializer):
    hotels = HotelSerializer(many=True, read_only=True)
    activities = ActivitySerializer(many=True, read_only=True)

    class Meta:
        model = Package
        fields = ['id', 'image', 'name', 'description', 'price', 'location', 'duration', 'availability', 'hotels', 'activities']


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

