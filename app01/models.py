from django.db import models

# Create your models here.
class Customer(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    choices = (
        (1, 'male'),
        (2, 'female')
    )
    gender = models.SmallIntegerField(choices=choices)
