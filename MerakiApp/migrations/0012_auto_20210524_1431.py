# Generated by Django 3.1.7 on 2021-05-24 08:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MerakiApp', '0011_shipping'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shipping',
            name='state',
        ),
        migrations.AddField(
            model_name='shipping',
            name='alternatenumber',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='shipping',
            name='contactnumebr',
            field=models.IntegerField(default=0),
        ),
    ]
