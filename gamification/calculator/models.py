from random import choices, seed
from .utils.box import get_loyalty, get_rentability,\
    convert_to_list, convert_to_dict, LOT_CATEGORIES

from django.db import models


seed(42)


class Product(models.Model):
    name = models.CharField(max_length=127)
    price = models.DecimalField(max_digits=7, decimal_places=2)

    class Meta:
        ordering = ('price',)

    def __str__(self):
        return self.name


class BlackBox(models.Model):
    name = models.CharField(max_length=127)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    loyalty = models.DecimalField(max_digits=3, decimal_places=2)
    rentability = models.DecimalField(max_digits=3, decimal_places=2)

    class Meta:
        ordering = ('price',)

    @classmethod
    def from_json(cls, data, instance=None):
        lot_cost = data.get('lot_cost')
        product_ids = data.get('product_ids')
        assert (lot_cost is None) != (product_ids is None)
        lot_amount = data['lot_amount']
        price = data['price']
        name = data['name']
        loyalty = get_loyalty(lot_amount)
        if lot_cost is not None:
            products = [Product.objects.create(name='mock', price=cost)
                        for cost in convert_to_list(lot_cost)]
            for product in products:
                product.save()
            rentability = get_rentability(lot_amount, lot_cost, price)
        else:
            products = [Product.objects.get(pk=pk) for pk in convert_to_list(product_ids)]
            prices = [product.price for product in products]
            rentability = get_rentability(lot_amount,
                                          convert_to_dict(prices),
                                          price)
        if instance is None:
            instance = BlackBox.objects.create(name=name, price=price,
                                               loyalty=loyalty, rentability=rentability)
        else:
            instance.name = name
            instance.price = price
            instance.loyalty = loyalty
            instance.rentability = rentability
            instance.items.all().delete()

        for product, amount in zip(products,
                                   convert_to_list(lot_amount)):
            item = BlackBoxItem.objects.create(product=product, black_box=instance, amount=amount)
            item.save()
        return instance

    def __str__(self):
        return f'Box({self.name}, {self.price}, {self.loyalty}, {self.rentability})'

    def products(self):
        return [item.product for item in self.sorted_items()]

    def probabilities(self):
        return [item.probability for item in self.sorted_items()]

    def sorted_items(self):
        return sorted(list(self.items.all()),
                      key=lambda item: item.product.price, reverse=True)

    def get_category_mapping(self):
        return {key:value for key, value in zip(self.products(), LOT_CATEGORIES)}

    def amounts(self):
        return [item.amount for item in self.sorted_items()]

    def lot_amount(self):
        amounts = [item.amount for item in self.sorted_items()]
        return {key:value for key, value in zip(LOT_CATEGORIES, amounts)}

    def lot_cost(self):
        costs = [item.product.price for item in self.sorted_items()]
        return {key:value for key, value in zip(LOT_CATEGORIES, costs)}

    def max_count_costly(self):
        return self.sorted_items()[0].amount

    def mock_open(self, n):
        """get an item from the box n times"""
        products = self.products()
        amounts = self.amounts()
        res = []
        total_giveaway = 0
        gained = 0
        for _ in range(n):
            gained += self.price
            valid_options = [i for i in range(3) if amounts[i] > 0 and total_giveaway + products[i].price <= gained]
            weights = [amounts[i] for i in valid_options]
            if len(valid_options) == 0:
                break
            i = choices(valid_options, weights=weights)[0]
            amounts[i] -= 1
            total_giveaway += products[i].price
            res.append(products[i])
        return res


class BlackBoxItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                related_name='items')
    black_box = models.ForeignKey(BlackBox, on_delete=models.CASCADE,
                                  related_name='items')
    amount = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return f'{self.product.name} in {self.black_box.name}'