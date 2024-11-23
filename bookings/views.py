from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Booking
from .serializers import BookingSerializer
from users.auth import admin_only

@api_view(['POST'])
def create_booking(request):
    if request.method == 'POST':
        serializer = BookingSerializer(data=request.data)
        if serializer.is_valid():
            # Additional logic for checking availability can be added here
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Package, Booking
from .forms import BookingForm

@login_required
def book_package(request, package_id):
    package = Package.objects.get(id=package_id)
    if not package.availability:
        # Handle unavailable package case
        return render(request, 'package_unavailable.html')

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.package = package
            booking.save()
            return redirect('booking_success')  # Redirect to a success page
    else:
        form = BookingForm(initial={'package': package})

    return render(request, 'bookings/bookings.html', {'form': form, 'package': package})

@login_required
@admin_only
def booking(request):
    items=Booking.objects.all()
    context={
        'items':items
    }
    return render(request,'bookings/bookings.html',context)