from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from datetime import date

class Patient(models.Model):
    patient_name = models.CharField(max_length=255)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10)
    NRCnum = models.CharField(max_length=255, unique=True)
    father_name = models.CharField(max_length=255)
    mother_name = models.CharField(max_length=255)
    guardian_name = models.CharField(max_length=255)
    relationship = models.CharField(max_length=255)
    address = models.TextField()
    insert_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='patients_inserted')
    last_edit_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='patients_last_edited')
    
    def __str__(self):
        return self.patient_name

class WaitingList(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    consult_date = models.DateField(default=date.today)  # Default to today's date
    queue_date_time = models.DateTimeField(auto_now_add=True)
    temperature = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    weight = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    blood_pressure = models.DecimalField(max_digits=20, decimal_places=2, null=True)
    insert_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='waiting_lists_inserted')
    last_edit_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='waiting_lists_last_edited')

    def __str__(self):
        return f"{self.patient.patient_name} - {self.consult_date}"
    
