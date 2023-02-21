######################################################################
# Copyright (c) 2023 Dmitry Pasichko. All rights reserved. #
######################################################################
from abc import ABC
from datetime import datetime

from .models import Order, Line
from .dtos import OrderDto, LineDto


class BaseService(ABC):
    def create(self, **kwargs):
        pass

    def update(self, **kwargs):
        pass

    def destroy(self):
        pass

    def get_by_pk(self, pk):
        pass


class LineService:
    @staticmethod
    def create_order_lines(order: Order, lines: dict) -> list[LineDto]:
        result = []
        for line_data in lines:
            product = line_data.get("product")
            quantity = line_data.get("quantity")
            success = product.write_off_product(quantity)
            line = Line.objects.create(
                **line_data,
                order=order,
                is_skipped=not success,
                product_price=product.price,
            )
            result.append(LineDto(line))
        return result


class OrderService(BaseService):
    order: Order = None

    def __init__(self, request, pk: int = None, order: Order = None) -> None:
        self.request = request
        if order:
            self.order = order
        elif pk:
            self.order = self.get_by_pk(pk)

    def create(self, **kwargs) -> Order:
        self.order = Order.objects.create(**kwargs)
        return self.order

    def update(self, **kwargs):
        for key, val in kwargs.items():
            setattr(self.order, key, val)

        self.order.save()

    def destroy(self):
        self.order.delete()

    def get_by_pk(self, pk: int) -> Order:
        return Order.objects.get(id__exact=pk)

    def prepare_calculated_fields(self, validated_data: dict) -> None:
        status = validated_data.get("status")
        if status in ["ACCEPTED", "DONE", "CANCELLED"]:

            def update_specific_status_date(status: str) -> tuple:
                now_date = datetime.now()
                match status:
                    case "CANCELLED":
                        key = "cancelled_date"
                    case "DONE":
                        key = "finish_date"
                    case "ACCEPTED":
                        key = "accepted_date"
                    case _:
                        key = None
                return key, now_date

            date_key, date_value = update_specific_status_date(status)
            validated_data[date_key] = date_value

        validated_data["creator"] = self.request.user

    @staticmethod
    def get_total_cost(lines: list[LineDto]) -> float:
        new_total_cost = 0
        for line in lines:
            if not line.is_skipped:
                new_total_cost += line.product_price * line.quantity
        return new_total_cost

    @staticmethod
    def get_queryset():
        return Order.objects.all()

    def create_order(
        self, order_validated_data: dict, lines_validated_data: dict
    ) -> dict:
        self.prepare_calculated_fields(order_validated_data)
        order = self.create(**order_validated_data)

        lines = LineService.create_order_lines(order, lines_validated_data)
        order.total_cost = self.get_total_cost(lines)
        order.save()
        return OrderDto(order).to_dict()
