# Generated by Django 3.1.7 on 2021-05-24 13:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('MerakiApp', '0016_auto_20210524_1501'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='transaction_id',
            new_name='orderid',
        ),
    ]
