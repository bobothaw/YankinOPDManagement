# Generated by Django 5.0.1 on 2024-02-07 16:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ReceptionApp', '0004_waitinglist_isready'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='waitinglist',
            name='blood_pressure',
        ),
        migrations.AddField(
            model_name='waitinglist',
            name='diastole',
            field=models.DecimalField(decimal_places=2, max_digits=5, null=True),
        ),
        migrations.AddField(
            model_name='waitinglist',
            name='systole',
            field=models.DecimalField(decimal_places=2, max_digits=5, null=True),
        ),
    ]
