from django.db import models

# Create your models here.

class ItemDimensions(models.Model):
    start_address = models.CharField(max_length=255)
    end_address = models.CharField(max_length=255)
    weight = models.IntegerField()
    