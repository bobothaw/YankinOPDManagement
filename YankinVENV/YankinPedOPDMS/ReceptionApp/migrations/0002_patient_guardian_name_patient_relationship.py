# Generated by Django 5.0.1 on 2024-02-03 18:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ReceptionApp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='patient',
            name='guardian_name',
            field=models.CharField(default='James', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='patient',
            name='relationship',
            field=models.CharField(default='Parent', max_length=255),
            preserve_default=False,
        ),
    ]
