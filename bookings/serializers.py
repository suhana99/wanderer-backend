# bookings/serializers.py
from rest_framework import serializers
from .models import Booking

class BookingSerializer(serializers.ModelSerializer):
    hotel_name = serializers.CharField(source='package.hotel.name', read_only=True, default=None)
    activity_name = serializers.CharField(source='package.activity.name', read_only=True, default=None)
    package_name = serializers.CharField(source='package.name', read_only=True)

    class Meta:
        model = Booking
        fields = [
            'id',
            'user',
            'package_name',
            'hotel_name',
            'activity_name',
            'number_of_people',
            'booking_date',
        ]
