# Generated by Django 3.1.7 on 2021-05-24 08:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('MerakiApp', '0012_auto_20210524_1431'),
    ]

    operations = [
        migrations.RenameField(
            model_name='shipping',
            old_name='contactnumebr',
            new_name='contactnumber',
        ),
    ]