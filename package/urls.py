from django.urls import path
from .views import *
urlpatterns = [
    path('featured/',Featured_list.as_view()),
    path('package/<int:pk>/',PackageDetail.as_view()),
    path('reviews/<int:pk>/', ReviewListCreate.as_view(), name='package-reviews'),
    path('',index),
    path('addPackage/',post_package),
    path('updatepackage/<int:Package_id>',update_package),
    path('deletepackage/<int:Package_id>',delete_package),
]

