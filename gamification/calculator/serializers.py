from rest_framework import serializers

from .models import Product, BlackBox, BlackBoxItem


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('name', 'price', 'image', 'url',)


class BlackBoxItemSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = BlackBoxItem
        fields = ('product', 'black_box', 'price', 'amount', 'probability',)


class BlackBoxSerializer(serializers.ModelSerializer):
    items = BlackBoxItemSerializer(many=True)
    class Meta:
        model = BlackBox
        fields = ('name', 'url', 'items',)


class BlackBoxCreateSerializer(serializers.HyperlinkedModelSerializer):
    products = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), many=True)
    probabilities = serializers.ListField(
        child=serializers.IntegerField(min_value=0, max_value=100),
        min_length = 3, max_length = 3
    )

    class Meta:
        model = BlackBox
        fields = ('name', 'products', 'probabilities',)
