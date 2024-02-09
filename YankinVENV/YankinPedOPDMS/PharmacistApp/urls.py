from django.urls import path
from .views import medicine_insert



urlpatterns = [
    path('medicineadd/', medicine_insert, name="medicineadd")
]



