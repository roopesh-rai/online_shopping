# Generated by Django 4.0.2 on 2022-03-14 10:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_rename_contactform_checkoutform'),
    ]

    operations = [
        migrations.RenameField(
            model_name='checkoutform',
            old_name='person',
            new_name='pmethod',
        ),
    ]
