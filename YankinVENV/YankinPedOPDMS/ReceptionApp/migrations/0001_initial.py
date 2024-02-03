# Generated by Django 5.0.1 on 2024-02-03 16:53

import datetime
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('patient_name', models.CharField(max_length=255)),
                ('date_of_birth', models.DateField()),
                ('gender', models.CharField(max_length=10)),
                ('NRCnum', models.CharField(max_length=255, unique=True)),
                ('father_name', models.CharField(max_length=255)),
                ('mother_name', models.CharField(max_length=255)),
                ('address', models.TextField()),
                ('insert_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='patients_inserted', to=settings.AUTH_USER_MODEL)),
                ('last_edit_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='patients_last_edited', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='WaitingList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('consult_date', models.DateField(default=datetime.date.today)),
                ('queue_date_time', models.DateTimeField(auto_now_add=True)),
                ('temperature', models.DecimalField(decimal_places=2, max_digits=5, null=True)),
                ('weight', models.DecimalField(decimal_places=2, max_digits=5, null=True)),
                ('blood_pressure', models.DecimalField(decimal_places=2, max_digits=20, null=True)),
                ('insert_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='waiting_lists_inserted', to=settings.AUTH_USER_MODEL)),
                ('last_edit_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='waiting_lists_last_edited', to=settings.AUTH_USER_MODEL)),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ReceptionApp.patient')),
            ],
        ),
    ]
