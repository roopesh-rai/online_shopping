# Generated by Django 4.0.3 on 2022-04-25 13:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='seller',
            name='rr',
        ),
    ]
