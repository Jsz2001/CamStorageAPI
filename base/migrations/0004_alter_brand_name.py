# Generated by Django 4.2.1 on 2023-05-18 05:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0003_alter_brand_name_alter_brand_website'),
    ]

    operations = [
        migrations.AlterField(
            model_name='brand',
            name='name',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
