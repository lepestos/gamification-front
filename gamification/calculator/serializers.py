from rest_framework import serializers

from .models import Product, BlackBox, BlackBoxItem


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('name', 'price', 'url',)


class BlackBoxItemSerializer(serializers.HyperlinkedModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = BlackBoxItem
        fields = ('product', 'black_box', 'amount',)


class BlackBoxSerializer(serializers.ModelSerializer):
    items = BlackBoxItemSerializer(many=True)

    class Meta:
        model = BlackBox
        fields = ('name', 'price', 'url', 'items',)


class BlackBoxCreateSerializer(serializers.HyperlinkedModelSerializer):
    products = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), many=True
    )
    amounts = serializers.ListField(
        child=serializers.IntegerField(min_value=0),
        min_length=3, max_length=3
    )

    class Meta:
        model = BlackBox
        fields = ('name', 'price', 'products', 'amounts',)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.price = validated_data.get('price', instance.price)
        products = validated_data.get('products', instance.products)
        amounts = validated_data.get('amounts', instance.probabilities)
        instance.items.all().delete()
        for product, amount in zip(products, amounts):
            item = BlackBoxItem.objects.create(product=product, black_box=instance,
                                               amount=amount)
            item.save()
        instance.save()
        return instance


class LotCostSerializer(serializers.Serializer):
    costly = serializers.DecimalField(min_value=0, max_digits=7, decimal_places=2)
    middle = serializers.DecimalField(min_value=0, max_digits=7, decimal_places=2)
    cheap = serializers.DecimalField(min_value=0, max_digits=7, decimal_places=2)


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