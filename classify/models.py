from django.db import models

# Create your models here.
class Image(models.Model):
    is_car = models.BooleanField()
    correct = models.BooleanField()
    source = models.CharField(max_length=50)