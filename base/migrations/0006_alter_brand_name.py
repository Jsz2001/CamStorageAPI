# Generated by Django 4.2.1 on 2023-05-20 04:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0005_brand_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='brand',
            name='name',
            field=models.CharField(max_length=100),
        ),
    ]