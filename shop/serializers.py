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
    class Meta:
        model = Line
        fields = ("product", "quantity")


class OrderSerializer(serializers.ModelSerializer):
    lines = OrderLineSerializer(source="shop_line_related", many=True)
    creator = serializers.PrimaryKeyRelatedField(read_only=True)
    total_cost = serializers.FloatField(read_only=True)

    class Meta:
        model = Order
        fields = "__all__"

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

    def create(self, validated_data):
        lines_data = validated_data.pop("shop_line_related")
        new_order = Order.objects.create(**validated_data)
        for line_data in lines_data:
            Line.objects.create(order=new_order, **line_data)

        new_order.update_total_cost()
        return new_order

    def update(self, instance, validated_data):
        new_order = super().update(instance, validated_data)
        if "status" in validated_data:
            new_order.update_specific_status_date()

        return new_order
