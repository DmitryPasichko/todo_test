######################################################################
# Copyright (c) 2023 Dmitry Pasichko. All rights reserved. #
######################################################################
from datetime import datetime

from .models import Product, Line, Order


class ProductDto:
    def __init__(self, product: Product):
        self.name: str = product.name
        self.price: int = product.price
        self.quantity_on_hand: int = product.quantity_on_hand

    def to_dict(self):
        return {
            "name": self.name,
            "price": self.price,
            "quantity_on_hand": self.quantity_on_hand,
        }


class LineDto:
    def __init__(self, line: Line):
        self.product: ProductDto = ProductDto(line.product)
        self.quantity: int = line.quantity
        self.is_skipped: bool = line.is_skipped
        self.product_price: float = line.product_price

    def to_dict(self):
        return {
            "product": self.product.to_dict(),
            "quantity": self.quantity,
            "is_skipped": self.is_skipped,
            "product_price": self.product_price,
        }


class OrderDto:
    def __init__(self, order: Order):
        self.total_cost: float = order.total_cost
        self.status: str = order.status
        self.creator: int = order.creator.pk
        self.finish_date: datetime = order.finish_date
        self.accepted_date: datetime = order.accepted_date
        self.cancelled_date: datetime = order.cancelled_date
        self.created: datetime = order.created
        self.lines: list[LineDto] = [
            LineDto(line) for line in order.shop_line_related.all()
        ]

    def to_dict(self):
        return {
            "total_cost": self.total_cost,
            "status": self.status,
            "creator": self.creator,
            "finish_date": self.finish_date,
            "accepted_date": self.accepted_date,
            "cancelled_date": self.cancelled_date,
            "created": self.created,
            "lines": [line.to_dict() for line in self.lines],
        }
