from random import choices, seed

from django.db import models


seed(42)


class Product(models.Model):
    name = models.CharField(max_length=127)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    time_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-time_created',)

    def __str__(self):
        return self.name


class BlackBox(models.Model):
    name = models.CharField(max_length=127)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    time_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-time_created',)

    def __str__(self):
        return self.name

    def products(self):
        return [item.product for item in self.items.all()]

    def probabilities(self):
        return [item.probability for item in self.items.all()]

    def amounts(self):
        return [item.amount for item in self.items.all()]

    def mock_open(self, n):
        """get an item from the box n times"""
        products = self.products()
        amounts = self.amounts()
        res = []
        for _ in range(n):
            valid_options = [i for i in range(3) if amounts[i] > 0]
            weights = [amounts[i] for i in range(3) if amounts[i] > 0]
            if len(valid_options) == 0:
                break
            i = choices(valid_options, weights=weights)[0]
            amounts[i] -= 1
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