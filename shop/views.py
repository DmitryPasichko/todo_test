from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.decorators import action


from .serializers import ProductSerializer, OrderSerializer
from .models import Product, Order


class BaseAuthorizedView(ModelViewSet):
    authentication_classes = [
        JWTAuthentication,
    ]
    permission_classes = (
        IsAuthenticatedOrReadOnly,
    )


class ProductView(BaseAuthorizedView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()


class OrderView(BaseAuthorizedView):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()

    # @action(
    #     detail=True,
    #     methods=["post"],
    #     permission_classes=(
    #             IsAuthenticated,
    #     ),
    #     url_path="update-status/(?P<status>[^/.]+)"
    # )
    # def update_status(self, request, pk=None, status=None):
    #     order = self.get_object()
    #     if status:

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)




