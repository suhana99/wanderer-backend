from django.urls import path
from .views import *

urlpatterns = [
    path('bookings/', create_booking, name='create_booking'),
    path('',booking),
]
