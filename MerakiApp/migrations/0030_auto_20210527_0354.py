# Generated by Django 3.1.7 on 2021-05-26 22:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('MerakiApp', '0029_auto_20210527_0300'),
    ]

    operations = [
        migrations.RenameField(
            model_name='shipping',
            old_name='customer',
            new_name='custome',
        ),
    ]
