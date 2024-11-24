from django.contrib import admin
from .models import Package, Hotel, Activity, Review

admin.site.register(Package)
class PackageAdmin(admin.ModelAdmin):
    list_display = ['name', 'location', 'price', 'duration', 'availability']
    filter_horizontal = ['hotels', 'activities']

admin.site.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = ['name', 'location', 'availability', 'owner']

admin.site.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ['name', 'location', 'availability', 'owner']

admin.site.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['package', 'user', 'rating', 'date_added']
