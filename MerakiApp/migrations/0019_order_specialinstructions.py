# Generated by Django 3.1.7 on 2021-05-24 16:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MerakiApp', '0018_auto_20210524_1943'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='specialinstructions',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]