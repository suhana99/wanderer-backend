from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Booking
from .serializers import BookingSerializer
from users.auth import admin_only
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

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
from package.models import Hotel, Activity

@login_required
def book_package(request, package_id,hotel_id,activity_id):
    package = Package.objects.get(id=package_id)
    hotels=Hotel.objects.get(id=hotel_id)
    activity=Activity.objects.get(id=activity_id) 
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

    return render(request, 'bookings/bookings.html', {'form': form, 'package': package, 'hotels':hotels, 'activity':activity})

@login_required
@admin_only
def booking(request):
    items=Booking.objects.all()
    context={
        'items':items
    }
    return render(request,'bookings/bookings.html',context)

class SellerDashboardView(ListAPIView):
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        # Hotel owners see bookings for their hotels
        if user.role == 'hotel_owner':
            return Booking.objects.filter(package__hotel__owner=user).select_related('package', 'user')

        # Activity listers see bookings for their activities
        elif user.role == 'activity_lister':
            return Booking.objects.filter(package__activity__owner=user).select_related('package', 'user')

        # Non-sellers or unauthorized users see nothing
        return Booking.objects.none()