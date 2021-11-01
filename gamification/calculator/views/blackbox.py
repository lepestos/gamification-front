from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from calculator.utils.box import Box
from calculator.models import BlackBox
from calculator.serializers.blackbox import BlackBoxSerializer,\
    CalculateSerializer, MockOpenSerializer, MockOpenUnsavedSerializer


class BlackBoxViewSet(viewsets.ModelViewSet):
    serializer_class = BlackBoxSerializer
    queryset = BlackBox.objects.all()

    def get_serializer_class(self):
        if self.action == 'calculate':
            return CalculateSerializer
        if self.action == 'mock_open':
            return MockOpenSerializer
        if self.action == 'mock_open_unsaved':
            return MockOpenUnsavedSerializer
        return super().get_serializer_class()

    def perform_create(self, serializer):
        box = BlackBox.from_json(serializer.data)
        box.save()

    def perform_update(self, serializer):
        instance = serializer.instance
        data = serializer.validated_data
        box = BlackBox.from_json(data, instance=instance)
        box.save()

    @action(detail=False, methods=['post'])
    def calculate(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            box = Box(**serializer.data)
            data = box.to_json()
            if data['success']:
                return Response(data)
            else:
                return Response(data, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def mock_open(self, request, pk):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            bb = BlackBox.objects.get(pk=pk)
            products = bb.mock_open(serializer.data.get('n'))
            cat_map = bb.get_category_mapping()
            data = {'product_categories': [cat_map[product] for product in products]}
            return Response(data)

        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def mock_open_unsaved(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            bb = BlackBox.from_json(serializer.data)
            bb.save()
            products = bb.mock_open(serializer.data.get('n'))
            cat_map = bb.get_category_mapping()
            data = {'product_categories': [cat_map[product] for product in products]}
            bb.delete()
            return Response(data)
