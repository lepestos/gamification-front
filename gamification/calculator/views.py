from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Product, BlackBoxItem, BlackBox
from .serializers import (ProductSerializer, BlackBoxItemSerializer,
                          BlackBoxSerializer, BlackBoxCreateSerializer,
                          CalculateSerializer, MockOpenSerializer)
from .box import Box, convert_to_dict


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
        amounts = serializer.data['amounts']
        price = serializer.data['price']
        box = BlackBox.objects.create(name=serializer.data['name'], price=price)
        for pk, am in zip(products, amounts):
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
            if box.get_rounded_max_price() < box.get_rounded_min_price():
                data = {
                    'message': 'Цены дорогого и среднего лотов '
                               'отличаются на слишком маленькую величину.'
                }
                return Response(data, status=status.HTTP_400_BAD_REQUEST)
            data = {
                'probabilities': convert_to_dict(box.probabilities),
                'amounts': convert_to_dict(box.amounts),
                'black_box_cost': {
                    'cur': box.get_rounded_ticket_price(),
                    'max': box.get_rounded_max_price(),
                    'min': box.get_rounded_min_price()
                },
                'message': box.message,
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
