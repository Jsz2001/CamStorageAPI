from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL


class Brand(models.Model):
    user = models.ForeignKey(User, default=1, null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=100)
    website = models.CharField(max_length=150, null=True, blank=True)

    def __str__(self):
        return self.name


class Camera(models.Model):
    #pk
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True, blank=True)    
    name = models.CharField(max_length=150)
    price = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    note = models.TextField(blank=True, null=True)


    def __str__(self):
        return self.name
    

class Gear(models.Model):

    class GearType(models.TextChoices):
        LENS = 'LEN',
        LIGHTING = 'LIGHT',
        BATTERY = 'BATTERY',
        MICROPHONE = 'MIC',
        TRIPOD = 'TRIPOD',
        OTHER = 'OTHER'


    user = models.ForeignKey(User, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True, blank=True)
    camera = models.ManyToManyField(Camera)
    name = models.CharField(max_length=150)
    gear_type = models.CharField(max_length=7, choices=GearType.choices, default=GearType.OTHER)
    price = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    quantity = models.IntegerField(default=1)
    note = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


