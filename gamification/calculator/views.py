from rest_framework import viewsets

from .models import Product, BlackBoxItem, BlackBox
from .serializers import (ProductSerializer, BlackBoxItemSerializer,
                          BlackBoxSerializer, BlackBoxCreateSerializer)

class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()


class BlackBoxItemViewSet(viewsets.ModelViewSet):
    serializer_class = BlackBoxItemSerializer
    queryset = BlackBoxItem.objects.all()


class BlackBoxViewSet(viewsets.ModelViewSet):
    serializer_class = BlackBoxSerializer
    queryset = BlackBox.objects.all()

    def get_serializer_class(self):
        if self.action == 'create':
            return BlackBoxCreateSerializer
        return super().get_serializer_class()

    def perform_create(self, serializer):
        products = serializer.data['products']
        probabilities = serializer.data['probabilities']
        box = BlackBox.objects.create(name=serializer.data['name'])
        for pk, prob in zip(products, probabilities):
            product = Product.objects.get(pk=pk)
            item = BlackBoxItem.objects.create(product=product, black_box=box,
                                               price=product.price, probability=prob)
            item.save()
        box.save()