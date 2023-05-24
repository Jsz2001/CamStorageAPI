# Generated by Django 4.2.1 on 2023-05-23 08:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0007_gear'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gear',
            name='gear_type',
            field=models.CharField(choices=[('LEN', 'Lens'), ('LIGHT', 'Lighting'), ('BATTERY', 'Battery'), ('MIC', 'Microphone'), ('TRIPOD', 'Tripod'), ('OTHER', 'Other')], default='OTHER', max_length=7),
        ),
    ]