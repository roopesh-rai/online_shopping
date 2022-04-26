from django.db import models
from django.contrib.auth.models import User
# Create your models here.

STAGE_CHOICES = (
    ('Starting a new business', 'Starting a new business'),
    ('Need More Information', 'Need More Information'),
    ('I sell on market places', 'I sell on market places')
)

COMPANY_SIZE_CHOICES =(
    ('1-10 Employees', '1-10 Employees'),
    ('11-50 Employees', '11-50 Employees'),
    ('51-200 Employees', '51-200 Employees'),
    ('201-500 Employees', '201-500 Employees'),
    ('500+ Employees', '500+ Employees'),
    ('Self Employed', 'Self Employed'),
)

STATE_CHOICES = (
    ('Andaman and Nicobar', 'Andaman and Nicobar'),
    ('Andhra Pradesh', 'Andhra Pradesh'),
    ('Arunachal Pradesh', 'Arunachal Pradesh'),
    ('Assam', 'Assam'),
    ('Bihar', 'Bihar'),
    ('Chandigarh', 'Chandigarh'),
    ('Chhattisgarh', 'Chhattisgarh'),
    ('Dadra and Nagar Haveli', 'Dadra and Nagar Haveli'),
    ('Daman and Diu', 'Daman and Diu'),
    ('Delhi', 'Delhi'),
    ('Goa', 'Goa'),
    ('Gujarat', 'Gujarat'),
    ('Haryana', 'Haryana'),
    ('Himachal Pradesh', 'Himachal Pradesh'),
    ('Jammu and Kashmir', 'Jammu and Kashmir'),
    ('Jharkhand', 'Jharkhand'),
    ('Karnataka', 'Karnataka'),
    ('Kerala', 'Kerala'),
    ('Lakshadweep', 'Lakshadweep'),
    ('Madhya Pradesh', 'Madhya Pradesh'),
    ('Maharashtra', 'Maharashtra'),
    ('Manipur', 'Manipur'),
    ('Meghalaya', 'Meghalaya'),
    ('Mizoram', 'Mizoram'),
    ('Nagaland', 'Nagaland'),
    ('Orissa', 'Orissa'),
    ('Puducherry', 'Puducherry'),
    ('Punjab', 'Punjab'),
    ('Rajesthan', 'Rajesthan'),
    ('Sikkim', 'Sikkim'),
    ('Tamil Nadu', 'Tamil Nadu'),
    ('Telangana', 'Telangana'),
    ('Tripura', 'Tripura'),
    ('Uttar Pradesh', 'Uttar Pradesh'),
    ('Uttarakhand', 'Uttarakhand'),
    ('West Bengal', 'West Bengal'),
)


class Seller(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # sno = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    phone = models.IntegerField(unique=True)
    email = models.EmailField(unique=True)
    stage_of_business = models.CharField(choices=STAGE_CHOICES, max_length=50)
    company_name = models.CharField(max_length=50)
    company_size = models.CharField(choices=COMPANY_SIZE_CHOICES, max_length=30)
    company_address = models.TextField()
    city = models.CharField(max_length=20)
    zipcode = models.CharField(max_length=6)
    state = models.CharField(choices=STATE_CHOICES, max_length=50)
    gst = models.CharField(max_length=15, unique=True)
    def __str__(self):
        return str(self.id)