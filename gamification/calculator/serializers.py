from rest_framework import serializers

from .models import Product, BlackBox, BlackBoxItem
from .utils.box import convert_to_list, get_loyalty, get_rentability


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('name', 'price', 'url',)


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
    lot_cost = LotCostSerializer
    lot_amount = LotAmountSerializer

    class Meta:
        model = BlackBox
        fields = ('name', 'price', 'loyalty', 'rentability',
                  'max_count_costly', 'lot_cost', 'lot_amount',)


class BlackBoxCreateSerializer(serializers.HyperlinkedModelSerializer):
    lot_cost = LotCostSerializer()
    lot_amount = LotAmountSerializer()

    class Meta:
        model = BlackBox
        fields = ('name', 'price', 'lot_cost', 'lot_amount')

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.price = validated_data.get('price', instance.price)
        lot_cost = validated_data.get('lot_cost', instance.lot_cost)
        lot_amount = validated_data.get('lot_amount', instance.lot_amount)
        instance.loyalty = get_loyalty(lot_amount)
        instance.rentability = get_rentability(lot_amount, lot_cost, instance.price)
        instance.items.all().delete()
        for cost, amount in zip(convert_to_list(lot_cost),
                                convert_to_list(lot_amount)):
            product = Product.objects.create(name='mock', price=cost)
            product.save()
            item = BlackBoxItem.objects.create(product=product, black_box=instance,
                                               amount=amount)
            item.save()
        instance.save()
        return instance

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