# Generated by Django 4.0.3 on 2022-04-25 13:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Seller',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=20)),
                ('last_name', models.CharField(max_length=20)),
                ('phone', models.IntegerField(unique=True)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('stage_of_business', models.CharField(choices=[('Starting a new business', 'Starting a new business'), ('Need More Information', 'Need More Information'), ('I sell on market places', 'I sell on market places')], max_length=50)),
                ('company_name', models.CharField(max_length=50)),
                ('company_size', models.CharField(choices=[('1-10 Employees', '1-10 Employees'), ('11-50 Employees', '11-50 Employees'), ('51-200 Employees', '51-200 Employees'), ('201-500 Employees', '201-500 Employees'), ('500+ Employees', '500+ Employees'), ('Self Employed', 'Self Employed')], max_length=30)),
                ('company_address', models.TextField()),
                ('city', models.CharField(max_length=20)),
                ('zipcode', models.CharField(max_length=6)),
                ('state', models.CharField(choices=[('Andaman and Nicobar', 'Andaman and Nicobar'), ('Andhra Pradesh', 'Andhra Pradesh'), ('Arunachal Pradesh', 'Arunachal Pradesh'), ('Assam', 'Assam'), ('Bihar', 'Bihar'), ('Chandigarh', 'Chandigarh'), ('Chhattisgarh', 'Chhattisgarh'), ('Dadra and Nagar Haveli', 'Dadra and Nagar Haveli'), ('Daman and Diu', 'Daman and Diu'), ('Delhi', 'Delhi'), ('Goa', 'Goa'), ('Gujarat', 'Gujarat'), ('Haryana', 'Haryana'), ('Himachal Pradesh', 'Himachal Pradesh'), ('Jammu and Kashmir', 'Jammu and Kashmir'), ('Jharkhand', 'Jharkhand'), ('Karnataka', 'Karnataka'), ('Kerala', 'Kerala'), ('Lakshadweep', 'Lakshadweep'), ('Madhya Pradesh', 'Madhya Pradesh'), ('Maharashtra', 'Maharashtra'), ('Manipur', 'Manipur'), ('Meghalaya', 'Meghalaya'), ('Mizoram', 'Mizoram'), ('Nagaland', 'Nagaland'), ('Orissa', 'Orissa'), ('Puducherry', 'Puducherry'), ('Punjab', 'Punjab'), ('Rajesthan', 'Rajesthan'), ('Sikkim', 'Sikkim'), ('Tamil Nadu', 'Tamil Nadu'), ('Telangana', 'Telangana'), ('Tripura', 'Tripura'), ('Uttar Pradesh', 'Uttar Pradesh'), ('Uttarakhand', 'Uttarakhand'), ('West Bengal', 'West Bengal')], max_length=50)),
                ('gst', models.CharField(max_length=15, unique=True)),
                ('rr', models.CharField(max_length=10)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
