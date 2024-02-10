import random
from faker import Faker
from django.contrib.auth.models import User
from .models import MedicineType, Medicine

fake = Faker()

# Define medicine types
medicine_types = ['Tablet', 'Antibiotic', 'Liquid', 'Injection', 'Cream']

# Create MedicineType objects
for type_name in medicine_types:
    MedicineType.objects.create(name=type_name)

# Generate fake data for Medicine objects
for _ in range(20):  # Number of medicines
    name = fake.word()
    type = random.choice(MedicineType.objects.all())
    dosage = random.uniform(0.1, 10.0)
    unit = random.choice(['mg', 'g', 'ml'])
    stock = random.randint(10, 1000)
    expiry_date = fake.future_date(end_date='+2y')
    manufacturer = fake.company()
    price_per_unit = random.uniform(1.0, 100.0)
    added_by = User.objects.first()  # Change this to the user who adds the medicines
    updated_by = User.objects.first()  # Change this to the user who updates the medicines

    # Create Medicine object
    Medicine.objects.create(
        name=name,
        type=type,
        dosage=dosage,
        unit=unit,
        stock=stock,
        expiry_date=expiry_date,
        manufacturer=manufacturer,
        price_per_unit=price_per_unit,
        added_by=added_by,
        updated_by=updated_by
    )
