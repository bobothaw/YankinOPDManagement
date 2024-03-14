# # from django.contrib.auth.models import User
# # from ReceptionApp.models import Patient
# # from faker import Faker
# # import random
from datetime import date
# # fake = Faker()

# # # Create a few sample users
# # users = User.objects.all()

# # # Populate the Patient model with sample data
# # for _ in range(30):
# #     Patient.objects.create(
# #         patient_name=fake.name(),
# #         date_of_birth=fake.date_of_birth(),
# #         gender=random.choice(['Male', 'Female']),
# #         NRCnum=fake.unique.random_number(digits=10),
# #         father_name=fake.first_name(),
# #         mother_name=fake.first_name(),
# #         guardian_name=fake.name(),
# #         relationship=fake.word(),
# #         address=fake.address(),
# #         insert_by=random.choice(users),
# #         last_edit_by=random.choice(users)
# #     )


# from django.contrib.auth.models import User
# from PharmacistApp.models import MedicineType, Medicine
# from faker import Faker
# import random

# fake = Faker()

# medicine_types = ['Tablet', 'Antibiotic', 'Liquid', 'Injection', 'Cream']

# for type_name in medicine_types:
#     MedicineType.objects.create(name=type_name)

# for _ in range(20):  
#     Medicine.objects.create(
#         name=fake.word(),
#         type=random.choice(MedicineType.objects.all()),
#         dosage=random.uniform(0.1, 10.0),
#         unit=random.choice(['mg', 'g', 'ml']),
#         stock=random.randint(10, 1000),
#         expiry_date=fake.future_date(end_date='+2y'),
#         manufacturer=fake.company(),
#         price_per_unit=random.uniform(1.0, 100.0),
#         added_by=User.objects.first(),
#         updated_by=User.objects.first()
#     )
print(date.today())