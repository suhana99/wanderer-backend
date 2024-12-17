from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import Hotel, Activity, Package, Review
from .serializers import HotelSerializer, ActivitySerializer, PackageSerializer, ReviewSerializer
from django.contrib.auth.decorators import login_required
from .forms import *
from users.auth import admin_only
from django.shortcuts import render,redirect
from django.contrib import messages


# Hotel Views
class HotelListCreateView(generics.ListCreateAPIView):
    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer
    permission_classes = [IsAuthenticated]


# Activity Views
class ActivityListCreateView(generics.ListCreateAPIView):
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer
    permission_classes = [IsAuthenticated]


# Package Views
class PackageListView(generics.ListAPIView):
    queryset = Package.objects.filter(availability=True)
    serializer_class = PackageSerializer


class PackageDetailView(generics.RetrieveAPIView):
    queryset = Package.objects.all()
    serializer_class = PackageSerializer


class CreatePackageView(generics.CreateAPIView):
    queryset = Package.objects.all()
    serializer_class = PackageSerializer
    permission_classes = [IsAdminUser]


# Review Views
class ReviewListCreateView(generics.ListCreateAPIView):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        package_id = self.kwargs['package_id']
        return Review.objects.filter(package_id=package_id)

    def perform_create(self, serializer):
        package = Package.objects.get(id=self.kwargs['package_id'])
        serializer.save(package=package, user=self.request.user)

@login_required
@admin_only
def index(request):
    #fetch data from the table
    packages=Package.objects.all()
    context={
        'packages':packages
    }
    return render(request,'packages/package.html',context)

@login_required
@admin_only
def post_package(request):
    if request.method=="POST":
        form=PackageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.add_message(request,messages.SUCCESS,'Package added successfully.')
            return redirect('/package/addPackage')
        else:
            messages.add_message(request,messages.ERROR,'failed to add Package.')
            return render(request,'/packages/addPackage.html',{'form':form})
    context={
        'form':PackageForm
    }
    return render(request,'packages/addPackage.html',context)

@login_required
@admin_only
def update_package(request,Package_id):
    instance=Package.objects.get(id=Package_id)

    if request.method=="POST":
        form=PackageForm(request.POST, request.FILES,instance=instance)
        if form.is_valid():
            form.save()
            messages.add_message(request,messages.SUCCESS,'Package updated successfully.')
            return redirect('/package/')
        else:
            messages.add_message(request,messages.ERROR,'failed to update Package.')
            return render(request,'/packages/updatePackage.html',{'form':form})
    context={
        'form':PackageForm(instance=instance)
    }
    return render(request,'packages/updatePackage.html',context)

@login_required
@admin_only
def delete_package(request,Package_id):
    package=Package.objects.get(id=Package_id)
    package.delete()
    messages.add_message(request,messages.SUCCESS,'Packages deleted.')
    return redirect('/package')

