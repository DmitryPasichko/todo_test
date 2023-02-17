from django.db import models
from django_countries.fields import CountryField


class Product(models.Model):
    name = models.CharField(max_length=50)
    price = models.PositiveIntegerField()
    discount = None  # Todo
    category = models.ForeignKey("Category", on_delete=models.CASCADE)
    country = CountryField()
    features = None  # Todo
    quantity_on_hand = models.PositiveSmallIntegerField()
    description = models.TextField()

    def __str__(self):
        return self.name
