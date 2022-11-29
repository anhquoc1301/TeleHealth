# Generated by Django 3.2.13 on 2022-11-29 15:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('medical_unit', '0001_initial'),
        ('address', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Doctor',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200)),
                ('gender', models.CharField(choices=[('man', 'Man'), ('woman', 'Woman')], max_length=20)),
                ('unsignedName', models.CharField(max_length=200)),
                ('is_accept', models.BooleanField(default=False)),
                ('detail_address', models.CharField(max_length=200)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now=True)),
                ('address', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='doctor', to='address.address')),
                ('medicalUnit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='doctor', to='medical_unit.medicalunit')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='doctor', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'doctor',
                'ordering': ['created_at'],
            },
        ),
    ]
