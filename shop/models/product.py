######################################################################
# Copyright (c) 2023 Dmitry Pasichko. All rights reserved. #
######################################################################
from django.db import models
from django_countries.fields import CountryField
from django.db import transaction


class Product(models.Model):
    name = models.CharField(max_length=50, unique=True)
    price = models.PositiveIntegerField()
    discount = None  # Todo
    category = models.ForeignKey("Category", on_delete=models.CASCADE)
    country = CountryField()
    features = None  # Todo
    quantity_on_hand = models.PositiveSmallIntegerField()
    description = models.TextField()

    def __str__(self):
        return self.name

    @property
    def available(self) -> bool:
        return self.quantity_on_hand > 0

    def is_product_acceptable_for_order(self, quantity: int) -> bool:
        return self.available and self.quantity_on_hand >= quantity

    def write_off_product(self, quantity: int) -> bool:
        success = True
        with transaction.atomic():
            if self.is_product_acceptable_for_order(quantity):
                self.quantity_on_hand -= quantity
                self.save()
            else:
                success = False
        return success


