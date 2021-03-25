from django.db import models

# Create your models here.
class NomuData(models.Model):
    client = models.CharField(max_length=500)
    sym = models.CharField(max_length=50)


class RecommendedItem(models.Model):
    clientName = models.CharField(max_length=500)
    sector = models.CharField(max_length=200)
    ticker = models.CharField(max_length=20)
    report = models.CharField(max_length=900)
    rating = models.CharField(max_length=10)
    ticks = models.FloatField(default=0.0)


class ClientAttributes(models.Model):
    clientName = models.CharField(max_length=500)
    revenueGrowth = models.FloatField(default=0.0)
    profitGrowth = models.FloatField(default=0.0)
    pbr = models.FloatField(default=0.0)
    per = models.FloatField(default=0.0)
    evtoEBITDA = models.FloatField(default=0.0)
    dividenYield = models.FloatField(default=0.0)


class SimilarClientItem(models.Model):
    clientName = models.CharField(max_length=500)
    sector = models.CharField(max_length=500)
    ticker = models.CharField(max_length=20)
    report = models.CharField(max_length=900)
    rating = models.CharField(max_length=10)
    ticks = models.FloatField(default=0.0)