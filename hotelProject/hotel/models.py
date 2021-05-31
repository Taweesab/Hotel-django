from os import name
from django.db import models

# Create your models here.
class hotel(models.Model):
    name = models.CharField(max_length=200)
    desc = models.TextField()






