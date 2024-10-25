from django.urls import path
from .views import *
urlpatterns=[
    path('dashboard/',dashboard),
    path('test/', test_view, name='test_view'),
    path('packages/',packages),
] 