from django.db import models


class Order(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    total_cost = models.FloatField()


class Line(models.Model):
    order = models.ForeignKey("Order", on_delete=models.CASCADE)
    product = models.ForeignKey("Product", on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField()
