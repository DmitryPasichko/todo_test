from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly


from .serializers import ProductSerializer
from .models import Product


class ProductView(ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    authentication_classes = [
        JWTAuthentication,
    ]
    permission_classes = (
        IsAuthenticatedOrReadOnly,
    )
