from rest_framework import serializers

from .models import Product, BlackBox, BlackBoxItem


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('name', 'price', 'image', 'url',)


class BlackBoxItemSerializer(serializers.HyperlinkedModelSerializer):
    product = ProductSerializer()
    class Meta:
        model = BlackBoxItem
        fields = ('product', 'black_box', 'price', 'amount', 'probability',)


class BlackBoxSerializer(serializers.ModelSerializer):
    items = BlackBoxItemSerializer(many=True)
    class Meta:
        model = BlackBox
        fields = ('name', 'url', 'items',)


class BlackBoxCreateSerializer(serializers.HyperlinkedModelSerializer):
    products = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), many=True
    )
    probabilities = serializers.ListField(
        child=serializers.IntegerField(min_value=0, max_value=100),
        min_length=3, max_length=3
    )

    class Meta:
        model = BlackBox
        fields = ('name', 'products', 'probabilities',)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        products = validated_data.get('products', instance.products)
        probabilities = validated_data.get('probabilities', instance.probabilities)
        instance.items.all().delete()
        for product, prob in zip(products, probabilities):
            item = BlackBoxItem.objects.create(product=product, black_box=instance,
                                               price=product.price, probability=prob)
            item.save()
        instance.save()
        return instance


class CalculateSerializer(serializers.Serializer):
    prices = serializers.ListField(
        child=serializers.DecimalField(min_value=0, max_digits=7, decimal_places=2),
        min_length=3, max_length=3
    )
    max_count_costly = serializers.IntegerField(min_value=0)
    profit = serializers.DecimalField(
        required=False, min_value=0, max_value=1, max_digits=3, decimal_places=2
    )
    loyalty = serializers.DecimalField(
        required=False, min_value=0, max_value=1, max_digits=3, decimal_places=2
    )
