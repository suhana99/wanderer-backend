from django.shortcuts import render,redirect
from rest_framework import generics,permissions,mixins,status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from .models import *
from .serializers import PackageSerializer,ReviewSerializer
from django.contrib import messages
from users.auth import admin_only
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http import JsonResponse
from django.db import IntegrityError
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from .forms import *

from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated


# Create your views here.

class AddHotelsActivitiesToPackageView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request, package_id):
        try:
            package = Package.objects.get(id=package_id)
        except Package.DoesNotExist:
            return Response({"error": "Package not found."}, status=status.HTTP_404_NOT_FOUND)

        hotels = request.data.get('hotels', [])
        activities = request.data.get('activities', [])

        # Add hotels
        if hotels:
            for hotel_id in hotels:
                try:
                    hotel = Hotel.objects.get(id=hotel_id)
                    package.hotels.add(hotel)
                except Hotel.DoesNotExist:
                    continue

        # Add activities
        if activities:
            for activity_id in activities:
                try:
                    activity = Activity.objects.get(id=activity_id)
                    package.activities.add(activity)
                except Activity.DoesNotExist:
                    continue

        package.save()
        return Response({"message": "Hotels and activities added to package successfully."}, status=status.HTTP_200_OK)
    
class Featured_list(generics.ListAPIView):
    queryset=Package.objects.all().order_by('-id')[:6]
    serializer_class=PackageSerializer

    def perform_create(self,serializer):
        serializer.save()

class PackageDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Package.objects.all()
    serializer_class = PackageSerializer


class ReviewListCreate(generics.ListCreateAPIView):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        package_id = self.kwargs['package_id']
        return Review.objects.filter(package_id=package_id)

    def perform_create(self, serializer):
        package_id = self.kwargs['package_id']
        try:
            package = Package.objects.get(id=package_id)
        except Package.DoesNotExist:
            raise ValidationError("Invalid package ID.")
        serializer.save(user=self.request.user, package=package)

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

# @login_required
# @admin_only
# def post_category(request):
#     if request.method=="POST":
#         form=CategoryForm(request.POST)
#         if form.is_valid():
#             form.save()
#             messages.add_message(request,messages.SUCCESS,'Category added successfully.')
#             return redirect('/Packages/addcategory')
#         else:
#             messages.add_message(request,messages.ERROR,'failed to add category.')
#             return render(request,'Packages/addcategory.html',{'form':form})
#     context={
#         'form':CategoryForm
#     }
#     return render(request,'Packages/addcategory.html',context)

# @login_required
# @admin_only
# def show_category(request):
#     #fetch data from the table
#     categories=Category.objects.all()
#     context={
#         'categories':categories
#     }
#     return render(request,'Packages/category.html',context)

# @login_required
# @admin_only
# def update_category(request,category_id):
#     instance=Category.objects.get(id=category_id)

#     if request.method=="POST":
#         form=CategoryForm(request.POST,instance=instance)
#         if form.is_valid():
#             form.save()
#             messages.add_message(request,messages.SUCCESS,'Category updated successfully.')
#             return redirect('/Packages/categories')
#         else:
#             messages.add_message(request,messages.ERROR,'failed to update category.')
#             return render(request,'Packages/updatecategory.html',{'form':form})
#     context={
#         'form':CategoryForm(instance=instance)
#     }
#     return render(request,'Packages/updatecategory.html',context)

# @login_required
# @admin_only
# def delete_category(request,category_id):
#     category=Category.objects.get(id=category_id)
#     category.delete()
#     messages.add_message(request,messages.SUCCESS,'Category deleted.')
#     return redirect('/Packages/categories')
