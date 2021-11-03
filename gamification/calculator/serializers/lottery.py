from rest_framework import serializers

from calculator.models import Lottery, Ticket, Product

from calculator.serializers.product import ProductSerializer


class TicketSerializer(serializers.HyperlinkedModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = Ticket
        fields = ('product',)


class LotterySerializer(serializers.ModelSerializer):
    ticket = TicketSerializer()
    product_ids = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())

    class Meta:
        model = Lottery
        fields = ('name', 'write_off', 'referral_coeff', 'ticket', 'product_ids')
        write_only = ('product_ids',)


class LotSerializer(serializers.Serializer):
    amount = serializers.IntegerField(min_value=1)
    price = serializers.DecimalField(min_value=0, max_digits=7, decimal_places=2)


class CalculateSerializer(serializers.Serializer):
    lots = serializers.ListField(
        child=LotSerializer(help_text='{amount : int, price : decimal}'))
    write_off = serializers.DecimalField(max_digits=7, decimal_places=2, required=False, allow_null=True)
    referral_coeff = serializers.DecimalField(max_digits=7, decimal_places=2, required=False)
    ticket_amount = serializers.IntegerField(min_value=0)
    ticket_price = serializers.DecimalField(max_digits=7, decimal_places=2, min_value=0)

