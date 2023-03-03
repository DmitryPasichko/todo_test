######################################################################
# Copyright (c) 2023 Dmitry Pasichko. All rights reserved. #
######################################################################
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, ListModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser
from rest_framework_simplejwt.authentication import JWTAuthentication
from django_filters.rest_framework import DjangoFilterBackend


from .services import OrderService
from .filters import TelegramUserFilter
from .models import Product, TelegramUser
from .serializers import ProductSerializer, OrderSerializer, UserSerializer


class BaseAuthorizedView(ModelViewSet):
    authentication_classes = [
        JWTAuthentication,
    ]
    permission_classes = (IsAuthenticatedOrReadOnly,)


class UserView(ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, GenericViewSet):
    authentication_classes = [
        JWTAuthentication,
    ]
    permission_classes = (IsAdminUser,)
    serializer_class = UserSerializer
    queryset = TelegramUser.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = TelegramUserFilter


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
