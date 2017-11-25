from django.db import models

# Create your models here.
class Ukazi(models.Model):
    smer = models.FloatField()
    hitrost = models.FloatField()