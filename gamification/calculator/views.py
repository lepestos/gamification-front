from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Product, BlackBoxItem, BlackBox
from .serializers import (ProductSerializer, BlackBoxItemSerializer,
                          BlackBoxSerializer, BlackBoxCreateSerializer,
                          CalculateSerializer,)
from .box import Box


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
        if self.action == 'calculate':
            return CalculateSerializer
        return super().get_serializer_class()

    def perform_create(self, serializer):
        products = serializer.data['products']
        amount = serializer.data['amount']
        box = BlackBox.objects.create(name=serializer.data['name'])
        for pk, am in zip(products, amount):
            product = Product.objects.get(pk=pk)
            item = BlackBoxItem.objects.create(product=product, black_box=box,
                                                amount=am)
            item.save()
        box.save()

    @action(detail=False, methods=['post'])
    def calculate(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            box = Box(**serializer.data)
            data = {
                'probabilities': box.probabilities,
                'amounts': box.amounts
            }
            return Response(data)

        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)