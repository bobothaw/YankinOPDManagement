from django.urls import path
from .views import medicine_insert, medicine_list

urlpatterns = [
    path('medicineadd/', medicine_insert, name="medicineadd"),
    path('medicine_list/', medicine_list, name="medicineList"),
]



