from django.urls import path
from .views import medicine_insert, medicine_list, medicine_edit

urlpatterns = [
    path('medicineadd/', medicine_insert, name="medicineadd"),
    path('medicine_list/', medicine_list, name="medicineList"),
    path('medicineEdit/<int:medicineID>/', medicine_edit, name="medicineEdit"),
]



