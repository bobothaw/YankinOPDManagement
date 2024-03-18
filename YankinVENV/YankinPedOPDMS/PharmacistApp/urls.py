from django.urls import path
from .views import medicine_insert, medicine_list, medicine_edit, prescribedList, presVerify

urlpatterns = [
    path('medicineadd/', medicine_insert, name="medicineadd"),
    path('medicine_list/', medicine_list, name="medicineList"),
    path('medicineEdit/<int:medicineID>/', medicine_edit, name="medicineEdit"),
    path('prescribed-list/', prescribedList, name="prescribedList"),
    path('verify-prescription/<int:diagID>', presVerify, name="presVerify"),
]



