# Generated by Django 3.1.7 on 2022-07-23 05:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('medical_unit', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='medicalunit',
            name='address',
        ),
    ]