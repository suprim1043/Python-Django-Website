# Generated by Django 3.1.7 on 2021-05-27 07:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MerakiApp', '0032_auto_20210527_1254'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shipping',
            name='alternatenumber',
            field=models.IntegerField(blank=True, default=' ', null=True),
        ),
        migrations.AlterField(
            model_name='shipping',
            name='contactnumber',
            field=models.IntegerField(blank=True, default=' ', null=True),
        ),
    ]
