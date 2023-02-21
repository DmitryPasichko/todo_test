######################################################################
# Copyright (c) 2023 Dmitry Pasichko. All rights reserved. #
######################################################################
from django.test import TestCase
from django.contrib.auth.models import User
from django.db.utils import IntegrityError
from rest_framework.test import APIClient, APITestCase

from shop.models import Product, Category

TEST_USER_NAME = "test_user"
TEST_USER_email = "test_user@yopmail.com"
TEST_USER_PASSWORD = "sdkgkp9oerw"


class ProductModelTestCase(TestCase):
    category1 = None
    category2 = None

    @classmethod
    def setUpTestData(cls):
        cls.category1 = Category.objects.create(name="category1")
        cls.category2 = Category.objects.create(name="category2")

    def test_create_product(self):
        product1 = Product.objects.create(
            name="product1",
            price=10,
            category=self.category1,
            country="US",
            quantity_on_hand=10,
            description="interesting thing",
        )

        self.assertEqual(
            product1.name,
            "product1",
            f"Product name is incorrect {product1.name} 'product1'",
        )
        self.assertEqual(
            product1.price, 10.0, f"Product price is incorrect {product1.price} '10.0'"
        )
        self.assertEqual(
            product1.category,
            self.category1,
            f"Product category is incorrect {product1.category} {self.category1}",
        )
        self.assertEqual(
            product1.country,
            "US",
            f"Product country is incorrect {product1.country} 'US'",
        )
        self.assertEqual(
            product1.quantity_on_hand,
            10,
            f"Product quantity_on_hand is incorrect {product1.quantity_on_hand} '10'",
        )
        self.assertEqual(
            product1.description,
            "interesting thing",
            f"Product description is incorrect {product1.description} 'interesting thing'",
        )

    def test_create_product_with_negative_amount(self):
        is_error = False
        try:
            Product.objects.create(
                name="product1",
                price=10,
                category=self.category1,
                country="US",
                quantity_on_hand=-10,
                description="interesting thing",
            )
        except IntegrityError as e:
            is_error = "shop_product_quantity_on_hand_check" in e.args[0]

        self.assertTrue(
            is_error, "Product has been created with negative quantity_on_hand"
        )

    def test_create_products_with_same_name(self):
        error = ""
        Product.objects.create(
            name="product1",
            price=10,
            category=self.category1,
            country="US",
            quantity_on_hand=10,
            description="interesting thing",
        )
        try:
            Product.objects.create(
                name="product1",
                price=10,
                category=self.category1,
                country="US",
                quantity_on_hand=10,
                description="interesting thing",
            )
        except IntegrityError as e:
            error = e.args[0]

        self.assertIn(
            "shop_product_name", error, "Product has been created with same name"
        )
        self.assertIn("_uniq", error, "Product has been created created with same name")


class ProductAPITestCase(APITestCase):
    client = APIClient()

    category1 = None
    category2 = None

    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(
            TEST_USER_NAME,
            email=TEST_USER_email,
            password=TEST_USER_PASSWORD,
        )

        cls.category1 = Category.objects.create(name="category1")
        cls.category2 = Category.objects.create(name="category2")

    def client_login(self):
        user = User.objects.get(username=TEST_USER_NAME)
        self.client.force_authenticate(user=user)
        # self.client.login(username=TEST_USER_NAME, password=TEST_USER_PASSWORD)

    def get_product_body(
        self, name, amount=10, description=None, price=10, is_category_instance=False
    ) -> dict:
        return dict(
            name=name,
            price=price,
            category=self.category1.pk if not is_category_instance else self.category1,
            country="US",
            quantity_on_hand=amount,
            description=description or "interesting thing",
        )

    def generate_products(self, product_count: int):
        for i in range(product_count):
            Product.objects.create(
                **self.get_product_body(
                    f"product{i}",
                    description=f"interesting thing{i}",
                    is_category_instance=True,
                )
            )

    @staticmethod
    def get_headers() -> dict:
        return {"Content-Type": "application/json", "Accept": "*/*"}

    def test_get_products(self):
        n_products = 4
        self.generate_products(n_products)
        response = self.client.get("/shop/product/")

        self.assertEqual(
            response.status_code,
            200,
            f"Expected 200 status but {response.status_code} was got",
        )
        self.assertEqual(
            len(response.data),
            n_products,
            f"Expected {n_products} status but {len(response.data)} was got",
        )

    def test_post_products(self):
        expected_success_status = 201
        expected_failed_status = 401
        product_data = self.get_product_body("product1")

        response = self.client.post("/shop/product/", data=product_data)
        self.assertEqual(
            response.status_code,
            expected_failed_status,
            f"Expected {expected_failed_status} status but {response.status_code} was got",
        )

        self.client_login()
        response = self.client.post("/shop/product/", data=product_data)
        self.assertEqual(
            response.status_code,
            expected_success_status,
            f"Expected {expected_success_status} status but {response.status_code} was got",
        )

    def test_post_equal_name_products(self):
        expected_failed_status = 400
        expected_error_msg = "product with this name already exists."
        error_field_name = "name"
        product_data = self.get_product_body("product1")

        self.client_login()
        self.client.post("/shop/product/", data=product_data)

        response = self.client.post("/shop/product/", data=product_data)
        self.assertEqual(
            response.status_code,
            expected_failed_status,
            f"Expected {expected_failed_status} status but {response.status_code} was got",
        )
        self.assertIn(
            error_field_name,
            response.data,
            f"Expected {error_field_name} is not present in response error",
        )
        self.assertEqual(
            str(response.data[error_field_name][0]),
            expected_error_msg,
            f"Expected {expected_error_msg} status but {str(response.data[error_field_name][0])} was got",
        )

    def test_post_negative_amount_products(self):
        expected_failed_status = 400
        expected_error_msg = "Ensure this value is greater than or equal to 0."
        error_field_name = "quantity_on_hand"
        product_data = self.get_product_body("product1", amount=-10)

        self.client_login()
        response = self.client.post("/shop/product/", data=product_data)
        self.assertEqual(
            response.status_code,
            expected_failed_status,
            f"Expected {expected_failed_status} status but {response.status_code} was got",
        )
        self.assertIn(
            error_field_name,
            response.data,
            f"Expected {error_field_name} is not present in response error",
        )
        self.assertEqual(
            str(response.data[error_field_name][0]),
            expected_error_msg,
            f"Expected {expected_error_msg} status but {str(response.data[error_field_name][0])} was got",
        )
