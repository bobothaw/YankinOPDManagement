from django.contrib.auth.models import User
from ReceptionApp.models import Patient
from faker import Faker
import random

fake = Faker()

# Create a few sample users
users = User.objects.all()

# Populate the Patient model with sample data
for _ in range(30):
    Patient.objects.create(
        patient_name=fake.name(),
        date_of_birth=fake.date_of_birth(),
        gender=random.choice(['Male', 'Female']),
        NRCnum=fake.unique.random_number(digits=10),
        father_name=fake.first_name(),
        mother_name=fake.first_name(),
        guardian_name=fake.name(),
        relationship=fake.word(),
        address=fake.address(),
        insert_by=random.choice(users),
        last_edit_by=random.choice(users)
    )
