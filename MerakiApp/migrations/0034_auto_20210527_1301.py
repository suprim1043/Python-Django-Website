# Generated by Django 3.1.7 on 2021-05-27 07:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MerakiApp', '0033_auto_20210527_1259'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shipping',
            name='alternatenumber',
            field=models.IntegerField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='shipping',
            name='contactnumber',
            field=models.IntegerField(blank=True, default=None, null=True),
        ),
    ]