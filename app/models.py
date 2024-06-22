from django.db import models


# Create your models here.
class Inventory(models.Model):
    name = models.CharField(max_length=255)
    text = models.TextField(max_length=255)
    quantity = models.IntegerField()


class Sales(models.Model):
    name = models.CharField(max_length=255)
    product_name = models.CharField(max_length=255)
    quantity = models.IntegerField()
    price = models.IntegerField()


class Customer(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.IntegerField()

