######################################################################
# Copyright (c) 2023 Dmitry Pasichko. All rights reserved. #
######################################################################

from rest_framework import serializers
from django.core.exceptions import ValidationError

from shop.models import *


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    available = serializers.ReadOnlyField()

    class Meta:
        model = Product
        fields = "__all__"


##############################################################


class OrderLineSerializer(serializers.ModelSerializer):
    price = serializers.SerializerMethodField(read_only=True)
    is_skipped = serializers.BooleanField(read_only=True)

    class Meta:
        model = Line
        fields = ("product", "quantity", "price", "is_skipped")

    def get_price(self, instance):
        return float(instance.product_price * instance.quantity)


class OrderLineFullSerializer(OrderLineSerializer):
    is_skipped = serializers.BooleanField(required=False)
    price = serializers.FloatField(required=False)

    class Meta:
        model = Line
        fields = ("product", "quantity", "price", "is_skipped", "product_price")


class OrderSerializer(serializers.ModelSerializer):
    lines = OrderLineSerializer(source="shop_line_related", many=True)
    creator = serializers.PrimaryKeyRelatedField(read_only=True)
    total_cost = serializers.FloatField(read_only=True)

    class Meta:
        model = Order
        fields = "__all__"

    def create(self, validated_data: dict):
        self.prepare_calculated_fields(validated_data)
        lines_data = validated_data.pop("shop_line_related")
        new_order = Order.objects.create(**validated_data)

        l_result = self.create_lines(lines_data, new_order)
        if l_result:
            new_order.total_cost = self.get_total_cost(l_result)
            new_order.save()

        return new_order

    def validate_status(self, status):
        if self.instance and self.instance.status in ["DONE", "CANCELLED"]:
            raise ValidationError("Sorry, order has been finished.")

        if (
            self.instance.status == "NEW"
            and status not in ["CANCELLED", "ACCEPTED"]
            or self.instance.status == "ACCEPTED"
            and status not in ["CANCELLED", "IN_PROGRESS"]
            or self.instance.status == "IN_PROGRESS"
            and status not in ["CANCELLED", "DONE"]
        ):
            raise ValidationError("Sorry, impossible to change status")
        return status

    @staticmethod
    def create_lines(lines: dict, new_order: Order) -> dict:
        for line_data in lines:
            line_data["order"] = new_order.pk
            line_data["product"] = line_data["product"].pk
        serializer = OrderLineFullSerializer(data=lines, many=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return serializer.data
        # for line_data in lines:
        #     product = line_data.get("product")
        #     quantity = line_data.get("quantity")
        #     success = product.write_off_product(quantity)
        #     Line.objects.create(**line_data, is_skipped=not success, order=new_order)

    @staticmethod
    def get_total_cost(lines: dict) -> float:
        new_total_cost = 0
        for line in lines:
            if not line["is_skipped"]:
                new_total_cost += line["product_price"] * line["quantity"]
        return new_total_cost
