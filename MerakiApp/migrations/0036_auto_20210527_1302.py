# Generated by Django 3.1.7 on 2021-05-27 07:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MerakiApp', '0035_auto_20210527_1301'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shipping',
            name='address',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='shipping',
            name='city',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
