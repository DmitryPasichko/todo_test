from datetime import datetime

from django.db import models
from django.db.models import signals

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

    def update_total_cost(self):
        new_total_cost = 0
        for line in self.shop_line_related.all():
            new_total_cost += line.product.price * line.quantity
        self.total_cost = new_total_cost
        self.save()

    def update_specific_status_date(self):
        now_date = datetime.now()
        match self.status:
            case "CANCELLED":
                self.cancelled_date = now_date
            case "DONE":
                self.finish_date = now_date
            case "ACCEPTED":
                self.accepted_date = now_date
            case _:
                pass
        self.save()


class Line(models.Model):
    order = models.ForeignKey("shop.Order", on_delete=models.CASCADE, related_name='%(app_label)s_%(class)s_related')
    product = models.ForeignKey("shop.Product", on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField()
