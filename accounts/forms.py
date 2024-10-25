from django.forms import ModelForm
from .models import Bookings
class BookingForm(ModelForm):
    class Meta:
        model=Bookings
        fields=['contact_no','address','payment_method']