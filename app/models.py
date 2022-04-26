from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
# Create your models here

class Contact(models.Model):
    sno = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=13)
    # person = models.CharField(choices=PERSON_CHOICES, max_length=50)
    person = models.CharField(max_length=50)
    context = models.TextField()

    def __str__(self):
        return str(self.sno)

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

class Customer(models.Model):
    user = models.OneToOneField(User, related_name='customer', on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    locality = models.CharField(max_length=20)
    city = models.CharField(max_length=20)
    zipcode = models.IntegerField()
    state = models.CharField(choices=STATE_CHOICES, max_length=50)

    def __str__(self):
        return str(self.id)

CATEGORY_CHOICES = (
    ('Mobiles', 'Mobiles'),
    ('Laptop', 'Laptop'),
    ('TopWear', 'TopWear'),
    ('BottomWear', 'BottomWear')
)

class Product(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    stripe_product_id = models.CharField(max_length=100)
    selling_price = models.FloatField()
    stripe_price_id = models.CharField(max_length=100)
    discounted_price = models.FloatField()
    description = models.TextField()
    brand = models.CharField(max_length=50)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=20)
    product_img = models.ImageField(upload_to='productimg')
    file = models.FileField(upload_to='product_files/', blank=True, null=True)
    url = models.URLField(blank=True, null=True)

    def __str__(self):
        return str(self.id)

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)

    @property
    def total_cost(self):
        return self.quantity * self.product.discounted_price

STATUS_CHOICES = (
    ('Accepted', 'Accepted'),
    ('Packed', 'Packed'),
    ('On The Way', 'On The Way'),
    ('Delivered', 'Delivered'),
    ('Cancel', 'Cancel')
)

class OrderPlaced(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    ordered_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(choices=STATUS_CHOICES, max_length=50, default='pending')

    def __str__(self):
        return str(self.id)

    @property
    def total_cost(self):
        return self.quantity * self.product.discounted_price


class checkoutform(models.Model):
    sno = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=13)
    pmethod = models.CharField(max_length=50)
    context = models.TextField()

    def __str__(self):
        return str(self.sno)

class Price(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    stripe_price_id = models.CharField(max_length=100)
    price = models.IntegerField(default=0)

class Invoice(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_id = models.CharField(max_length=122)
    payment_method = models.CharField(max_length=122)
    payment_status = models.CharField(max_length=122)
    total_amount = models.FloatField(max_length=122)
    shipping_charge = models.FloatField(default=70.00)


class InvoiceItems(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="invoice_product")
    product_price = models.FloatField(default=0)
