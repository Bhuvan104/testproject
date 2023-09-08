from django.db import models

# Create your models here.
from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()

class character(models.Model):
    character_name = models.CharField(max_length=100)
    address = models.TextField()
    phonenumber = models.TextField()
    def __str__(self):
        return self.character_name
    
class movie(models.Model):
    movie_name = models.CharField(max_length=100)
    character = models.ManyToManyField('character')
    rating = models.IntegerField()
    description = models.TextField()
    def __str__(self):
        return self.movie_name

from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()

    def __str__(self):
        return self.name
