######################################################################
# Copyright (c) 2023 Dmitry Pasichko. All rights reserved. #
######################################################################
from django.db import models

from ..validators import validate_line_quantity

ORDER_STATUSES = [
    ("NEW", "NEW"),
    ("READY", "READY"),
    ("ACCEPTED", "ACCEPTED"),
    ("IN_PROGRESS", "IN PROGRESS"),
    ("DONE", "DONE"),
    ("CANCELLED", "CANCELLED"),
]

DONE_STATUS = 'DONE'
ACCEPTED_STATUS = 'ACCEPTED'
CANCELLED_STATUS = 'CANCELLED'


class Order(models.Model):
    total_cost = models.FloatField(default=0)

    status = models.CharField(choices=ORDER_STATUSES, default="NEW", max_length=30)

    creator = models.ForeignKey("auth.User", on_delete=models.CASCADE)

    finish_date = models.DateTimeField(null=True, blank=True)
    accepted_date = models.DateTimeField(null=True, blank=True)
    cancelled_date = models.DateTimeField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created", "status"]


class Line(models.Model):
    order = models.ForeignKey("shop.Order", on_delete=models.CASCADE, related_name='%(app_label)s_%(class)s_related')
    product = models.ForeignKey("shop.Product", on_delete=models.CASCADE, related_name='%(app_label)s_%(class)s_related')
    quantity = models.PositiveSmallIntegerField(validators=[validate_line_quantity])
    is_skipped = models.BooleanField(default=False)
    product_price = models.FloatField(default=0)
