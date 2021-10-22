from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Product, BlackBoxItem, BlackBox
from .serializers import (ProductSerializer, BlackBoxItemSerializer,
                          BlackBoxSerializer, BlackBoxCreateSerializer,
                          CalculateSerializer, MockOpenSerializer)
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
        if self.action in ['create', 'update']:
            return BlackBoxCreateSerializer
        if self.action == 'calculate':
            return CalculateSerializer
        if self.action == 'mock_open':
            return MockOpenSerializer
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

    @action(detail=True, methods=['post'])
    def mock_open(self, request, pk):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            bb = BlackBox.objects.get(pk=pk)
            products = bb.mock_open(serializer.data.get('n'))
            data = {'product_names': [product.name for product in products]}
            return Response(data)

        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)