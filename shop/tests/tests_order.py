######################################################################
# Copyright (c) 2023 Dmitry Pasichko. All rights reserved. #
######################################################################
from django.contrib.auth.models import User
from django.db.models import QuerySet
from rest_framework.test import APIClient, APITestCase

from shop.models import Product, Order, Category

TEST_USER_NAME = "test_user"
TEST_USER_email = "test_user@yopmail.com"
TEST_USER_PASSWORD = "sdkgkp9oerw"

PRODUCT1_PRICE = 10
PRODUCT2_PRICE = 20
PRODUCT1_AMOUNT = 10
PRODUCT2_AMOUNT = 20
PRODUCT1_NAME = "Product1"
PRODUCT2_NAME = "Product2"


def get_product_body(name, category, amount=10, description=None, price=10) -> dict:
    return dict(
        name=name,
        price=price,
        category=category,
        country="US",
        quantity_on_hand=amount,
        description=description or "interesting thing",
    )


class OrderAPITestCase(APITestCase):
    client = APIClient()
    user = None

    category1 = None
    category2 = None
    product1 = None
    product2 = None

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            TEST_USER_NAME,
            email=TEST_USER_email,
            password=TEST_USER_PASSWORD,
        )

        cls.category1 = Category.objects.create(name="category1")
        cls.category2 = Category.objects.create(name="category2")
        cls.product1 = Product.objects.create(
            **get_product_body(
                PRODUCT1_NAME,
                cls.category1,
                amount=PRODUCT1_AMOUNT,
                price=PRODUCT1_PRICE,
            )
        )
        cls.product2 = Product.objects.create(
            **get_product_body(
                PRODUCT2_NAME,
                cls.category1,
                amount=PRODUCT2_AMOUNT,
                price=PRODUCT2_PRICE,
            )
        )

    def client_login(self) -> None:
        user = User.objects.get(username=TEST_USER_NAME)
        self.client.force_authenticate(user=user)

    def generate_orders(self, product_count: int) -> QuerySet:
        orders = Order.objects.bulk_create(
            [Order(creator=self.user) for x in range(product_count)]
        )

        return orders

    def test_get_order(self):
        n_order = 4
        self.generate_orders(n_order)
        response = self.client.get("/shop/order/")

        self.assertEqual(
            response.status_code,
            200,
            f"Expected 200 status but {response.status_code} was got",
        )
        self.assertEqual(
            len(response.data),
            n_order,
            f"Expected {n_order} status but {len(response.data)} was got",
        )

    def test_post_order(self):
        expected_success_status = 201
        expected_failed_status = 401
        payload = {"lines": [{"product": self.product2.id, "quantity": 2}]}

        response = self.client.post("/shop/order/", data=payload)
        self.assertEqual(
            response.status_code,
            expected_failed_status,
            f"Expected {expected_failed_status} status but {response.status_code} was got",
        )

        self.client_login()
        response = self.client.post("/shop/order/", data=payload)
        self.assertEqual(
            response.status_code,
            expected_success_status,
            f"Expected {expected_success_status} status but {response.status_code} was got",
        )
