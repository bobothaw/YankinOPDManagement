from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class MedicineType(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Medicine(models.Model):
    name = models.CharField(max_length=100)
    type = models.ForeignKey(MedicineType, on_delete=models.CASCADE)
    dosage = models.DecimalField(max_digits=10, decimal_places=2)
    unit = models.CharField(max_length=10)
    stock = models.DecimalField(max_digits=10, decimal_places=2)
    expiry_date = models.DateField()
    manufacturer = models.CharField(max_length=100)
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2)
    added_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mediciness_inserted')
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mediciness_updated')

    def __str__(self):
        return self.name

