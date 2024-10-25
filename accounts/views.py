from django.shortcuts import render,redirect
from .models import *
from django.contrib import messages
from  .forms import BookingForm
from django.urls import reverse
from django.views import View
from package.serializers import PackageSerializer
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response


from django.contrib.auth.decorators import login_required
from package.models import *

def index(request):
    return redirect('/home/')

def package(request):
   return redirect('/packages/')

@api_view(['GET'])
def packagedetail(request, package_id):
    package = get_object_or_404(Package, id=package_id)
    serializer = PackageSerializer(package)
    return Response(serializer.data)



@login_required
def wishlist(request,package_id):
    user = request.user
    package = Package.objects.get(id=package_id)
    check_items_presence=wishlist.objects.filter(user=user,package=package)
    if(check_items_presence):
        messages.add_message(request,messages.ERROR,'Package is already in the wishlist.')
        return redirect('/wishlist/')    #need to make wishlist.jsx
    else:
        wishlist=wishlist.objects.create(package=package,user=user)
        if wishlist:
            messages.add_message(request,messages.SUCCESS,'package added to the wishlist successfully.')
            return redirect('/wishlist')
        else:
            messages.add_message(request.messages.ERROR,'Something went wrong')


#need wishlist serializer as well

@login_required
def show_wishlist_items(request):
    user=request.user
    items=Wishlist.objects.filter(user=user)

    context={
        'items':items
    }
    return render(request,'users/wishlist.html',context)

@login_required
def remove_wishlist_item(request, wishlist_id):
    item=Wishlist.objects.get(id=wishlist_id)
    item.delete()
    messages.add_message(request,messages.SUCCESS,"Item removed successfully")
    return redirect('/wishlist')

@login_required
def booking_form(request,package_id,wishlist_id):
    user=request.user
    package=package.objects.get(id=package_id)
    wishlist_items=Wishlist.objects.get(id=wishlist_id)

    if request.method=="POST":
        form=BookingForm(request.POST)
        if form.is_valid():
            price=package.package_price
            total_price=int(price)
            contact_no=request.POST.get('contact_no')
            address=request.POST.get('address')
            payment_method=request.POST.get('payment_method')
            payment_status=request.POST.get('payment_status')


            #esma chai form create garera matra save garna milyo
            booking=Bookings.objects.create(
                package=package,
                user=user,
                total_price=total_price,
                contact_no=contact_no,
                address=address,
                payment_method=payment_method,
                payment_status=payment_status
            )
            #models ma j cha tei naam
            if booking.payment_method=='Cash on Delivery':
                wishlist_items.delete()
                messages.add_message(request,messages.SUCCESS,'booked successfully')
                return redirect('/wishlist/')
            elif booking.payment_method=='Esewa':
                return redirect(reverse('esewaform')+"?o_id="+str(booking.id)+"&c_id="+str(wishlist_items.id))
            else:
                messages.add_message(request,messages.ERROR,'Failed to place booking')
                return render(request,'users/bookingform.html',{'form':form})

    context={
        'form':BookingForm
    }
    return render(request,'users/bookingform.html',context)

import hmac
import hashlib
import uuid #to generate random string
import base64

class EsewaView(View):
    def get(self,request,*args,**kwargs):
        o_id=request.GET.get('o_id')
        c_id=request.GET.get('c_id')
        wishlist=Wishlist.objects.get(id=c_id)
        booking=Bookings.objects.get(id=o_id)

        uuid_val=uuid.uuid4()

        def genSha256(key,message):
            key=key.encode('utf-8')
            message=message.encode('utf-8')
            hmac_sha256=hmac.new(key,message,hashlib.sha256)

            digest=hmac_sha256.digest()

            signature=base64.b64encode(digest).decode('utf-8')
            return signature
        
        secret_key='8gBm/:&EnhH.1/q'
        data_to_assign=f"total_amount={booking.total_price},transaction_uuid={uuid_val},package_code=EPAYTEST"

        result=genSha256(secret_key,data_to_assign)

        data={
            'amount':booking.package.package_price,
            'total_amount':booking.total_price,
            'transaction_uuid':uuid_val,
            'package_code':'EPAYTEST',
            'signature':result
        }
        context={
            'booking':booking,
            'data':data,
            'wishlist':wishlist
        }
        return render(request,'users/esewaform.html',context)
    

import json
@login_required
def esewa_verify(request,booking_id,wishlist_id):
    if request.method=="GET":
        data=request.GET.get('data')
        decoded_data=base64.b64decode(data).decode()
        map_data=json.loads(decoded_data)
        booking=booking.objects.get(id=booking_id)
        wishlist=wishlist.objects.get(id=wishlist_id)

        if map_data.get('status')=='COMPLETE':
            booking.payment_status=True
            booking.save()
            wishlist.delete()
            messages.add_message(request,messages.SUCCESS,'Payment successful.')
            return redirect('/mybooking')
        
        else:
            messages.add_message(request,messages.ERROR,'Failed to make payment')
            return redirect('/mybooking')

@login_required
def my_booking(request):
    user=request.user
    items=Bookings.objects.filter(user=user)
    context={
        'items':items
    }
    return render(request,'users/mybooking.html',context)
    