from rest_framework import serializers

from calculator.models import BlackBoxItem, BlackBox
from calculator.serializers.product import ProductSerializer


class BlackBoxItemSerializer(serializers.HyperlinkedModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = BlackBoxItem
        fields = ('product', 'black_box', 'amount',)


class LotAmountSerializer(serializers.Serializer):
    costly = serializers.IntegerField()
    middle = serializers.IntegerField()
    cheap = serializers.IntegerField()


class LotCostSerializer(serializers.Serializer):
    costly = serializers.DecimalField(min_value=0, max_digits=7, decimal_places=2)
    middle = serializers.DecimalField(min_value=0, max_digits=7, decimal_places=2)
    cheap = serializers.DecimalField(min_value=0, max_digits=7, decimal_places=2)


class BlackBoxSerializer(serializers.ModelSerializer):
    lot_cost = LotCostSerializer()
    lot_amount = LotAmountSerializer()

    class Meta:
        model = BlackBox
        fields = ('name', 'price', 'lot_cost', 'lot_amount',
                  'loyalty', 'rentability', 'max_count_costly',)
        read_only_fields = ('loyalty', 'rentability', 'max_count_costly',)


class CalculateSerializer(serializers.Serializer):
    lot_cost = LotCostSerializer(help_text='{costly: float, middle: float, cheap: float}')
    costly_amount = serializers.IntegerField(min_value=0)
    rentability = serializers.DecimalField(required=False, min_value=0, max_value=1,
                                           max_digits=3, decimal_places=2,
                                           help_text="Десятичная дробь, не проценты!")
    loyalty = serializers.DecimalField(required=False, min_value=0, max_value=1,
                                       max_digits=3, decimal_places=2,
                                       help_text="Десятичная дробь, не проценты!")
    black_box_cost = serializers.DecimalField(min_value=0, max_digits=7, decimal_places=2)


class MockOpenSerializer(serializers.Serializer):
    n = serializers.IntegerField(min_value=1)


class MockOpenUnsavedSerializer(serializers.ModelSerializer):
    lot_cost = LotCostSerializer()
    lot_amount = LotAmountSerializer()
    n = serializers.IntegerField(min_value=1)

    class Meta:
        model = BlackBox
        fields = ('name', 'price', 'lot_cost', 'lot_amount', 'n')