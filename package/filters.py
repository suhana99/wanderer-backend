import django_filters
from .models import Package
class ProductFilter(django_filters.FilterSet):
    class Meta:
        model = Package
        fields = {
            'location':['exact'],
            'duration': ['lt', 'gt'],
            'price': ['lt', 'gt'],
        }