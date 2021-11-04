from rest_framework import serializers

from calculator.models import Lottery, Product


class LotterySerializer(serializers.ModelSerializer):
    product_ids = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())

    class Meta:
        model = Lottery
        fields = ('name', 'write_off', 'referral_coeff', 'product_ids')
        write_only = ('product_ids',)


class LotSerializer(serializers.Serializer):
    amount = serializers.IntegerField(min_value=1)
    price = serializers.DecimalField(min_value=0, max_digits=7, decimal_places=2)


class CalculateSerializer(serializers.Serializer):
    lots = LotSerializer(many=True)
    write_off = serializers.DecimalField(max_digits=7, decimal_places=2, min_value=0)
    referral_coeff = serializers.IntegerField(required=False)
    ticket_amount = serializers.IntegerField(min_value=0)
    ticket_price = serializers.DecimalField(max_digits=7, decimal_places=2, min_value=0)
