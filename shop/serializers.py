######################################################################
# Copyright (c) 2023 Dmitry Pasichko. All rights reserved. #
######################################################################

from rest_framework import serializers
from django.core.exceptions import ValidationError

from shop.models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = TelegramUser
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "phone",
            "external_id",
            "country",
            "language",
            "balance",
        )


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
