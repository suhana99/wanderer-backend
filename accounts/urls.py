from django.urls import path
from . import views
from .views import *
urlpatterns = [
    path('', views.index, name='index'),  # Home page redirect
    path('packages/', views.package, name='packages'),  # Redirect to packages

    # Package details
    path('packages/<int:package_id>/', views.packagedetail, name='package-detail'),  # Package detail API

    # Wishlist-related actions
    path('wishlist/add/<int:package_id>/', views.wishlist, name='add-to-wishlist'),  # Add package to wishlist
    path('wishlist/', views.show_wishlist_items, name='show-wishlist'),  # Show user's wishlist
    path('wishlist/remove/<int:wishlist_id>/', views.remove_wishlist_item, name='remove-wishlist-item'),  # Remove item from wishlist

    # Booking-related actions
    path('booking/<int:package_id>/<int:wishlist_id>/', views.booking_form, name='booking-form'),  # Booking form
    path('mybooking/', views.my_booking, name='my-booking'),  # Show user's bookings

    # Esewa payment
    path('esewaform/', EsewaView.as_view(), name='esewaform'),  # Esewa payment form
    path('esewa-verify/<int:booking_id>/<int:wishlist_id>/', views.esewa_verify, name='esewa-verify'),  # Verify Esewa payment
]