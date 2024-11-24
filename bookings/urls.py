from django.urls import path
from .views import *

urlpatterns = [
    path('bookings/', create_booking, name='create_booking'),
    path('',booking),
    path('seller-dashboard/', SellerDashboardView.as_view(),name='seller-dashboard'),
]
