from django.db import models
from ReceptionApp.models import WaitingList
from django.contrib.auth.models import User
from PharmacistApp.models import Medicine

# Create your models here.
class Ward(models.Model):
    ward_name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.ward_name
    
class Diagnosis(models.Model):
    diagnosis_name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.diagnosis_name
    
class DiagnosisDetails(models.Model):
    chief_conplaint = models.CharField(max_length=500)
    secondary_conplaint = models.CharField(max_length=200, null=True)
    physical_findings = models.CharField(max_length=500)
    test_results=models.CharField(max_length=200, null=True)
    primary_diagnosis = models.ForeignKey(Diagnosis, related_name='primary_diagnosis_details', on_delete=models.SET_NULL, null=True)
    secondary_diagnosis = models.ForeignKey(Diagnosis, related_name='secondary_diagnosis_details', on_delete=models.SET_NULL, null=True)
    waitingList = models.ForeignKey(WaitingList, on_delete=models.SET_NULL, null=True)
    diagnosed_datetime = models.DateTimeField(auto_now_add=True)
    diagnosedBy = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name = 'diagnosisdoctor')
    is_prescription_denied = models.BooleanField(null=True, blank=True)
    prescription_approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name = 'approvepharmacist')

    def __str__(self):
        return self.cheif_conplaint
    
class Admission(models.Model):
    admission_reason = models.CharField(max_length=300)
    admitted_ward = models.ForeignKey(Ward, on_delete=models.CASCADE)
    related_diag_detail = models.ForeignKey(DiagnosisDetails, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.admission_reason


class PrescribedMedicine(models.Model):
    relatedDiagDetail = models.ForeignKey(DiagnosisDetails, on_delete=models.CASCADE)
    medicine = models.ForeignKey(Medicine, on_delete=models.SET_NULL, null=True)
    quantity = models.DecimalField(max_digits=8, decimal_places=2)
    instruction = models.CharField(max_length=200)

    def __str__(self):
        return self.instruction







