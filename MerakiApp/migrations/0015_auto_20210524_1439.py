# Generated by Django 3.1.7 on 2021-05-24 08:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MerakiApp', '0014_auto_20210524_1438'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shipping',
            name='alternatenumber',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='shipping',
            name='contactnumber',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
