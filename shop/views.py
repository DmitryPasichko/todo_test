######################################################################
# Copyright (c) 2023 Dmitry Pasichko. All rights reserved. #
######################################################################
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework_simplejwt.authentication import JWTAuthentication


from .models import Product
from .services import OrderService
from .serializers import ProductSerializer, OrderSerializer


class BaseAuthorizedView(ModelViewSet):
    authentication_classes = [
        JWTAuthentication,
    ]
    permission_classes = (IsAuthenticatedOrReadOnly,)


class ProductView(BaseAuthorizedView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()


class OrderView(BaseAuthorizedView):
    serializer_class = OrderSerializer
    queryset = OrderService.get_queryset()

    def create(self, request, *args, **kwargs):
        order_serializer = self.get_serializer(data=request.data)
        order_serializer.is_valid(raise_exception=True)
        order_validated_data = order_serializer.validated_data
        lines_validated_data = order_validated_data.pop("shop_line_related")

        service = OrderService(request)

        result = service.create_order(order_validated_data, lines_validated_data)
        headers = self.get_success_headers(result)
        return Response(result, status=status.HTTP_201_CREATED, headers=headers)
