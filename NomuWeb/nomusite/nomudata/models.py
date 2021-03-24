from django.db import models

# Create your models here.
class NomuData(models.Model):
    client = models.CharField(max_length=500)
    sym = models.CharField(max_length=50)