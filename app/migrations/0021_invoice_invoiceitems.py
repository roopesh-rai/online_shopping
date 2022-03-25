# Generated by Django 4.0.3 on 2022-03-25 14:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0020_alter_product_file'),
    ]

    operations = [
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_id', models.CharField(max_length=122)),
                ('payment_method', models.CharField(max_length=122)),
                ('payment_status', models.CharField(max_length=122)),
                ('total_amount', models.FloatField(max_length=122)),
                ('shipping_charge', models.FloatField(default=70.0)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='InvoiceItems',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_price', models.FloatField(default=0)),
                ('invoice', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.invoice')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='invoice_product', to='app.product')),
            ],
        ),
    ]
