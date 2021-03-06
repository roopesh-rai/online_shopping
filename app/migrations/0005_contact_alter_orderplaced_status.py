# Generated by Django 4.0.2 on 2022-03-09 08:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_alter_product_category'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('sno', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('phone', models.CharField(max_length=13)),
                ('person', models.CharField(max_length=50, verbose_name=(('Mr Roopesh Rai', 'Mr Roopesh Rai'), ('Mr Om Ahuja', 'Mr Om Ahuja'), ('Mr Anand Tank', 'Mr Anand Tank')))),
                ('context', models.TextField()),
            ],
        ),
        migrations.AlterField(
            model_name='orderplaced',
            name='status',
            field=models.CharField(choices=[('Accepted', 'Accepted'), ('Packed', 'Packed'), ('On The Way', 'On The Way'), ('Delivered', 'Delivered'), ('Cancel', 'Cancel')], default='pending', max_length=50),
        ),
    ]
