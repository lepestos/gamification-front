from collections import Counter

from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from calculator.models import Product, BlackBox, BlackBoxItem


class MockOpenTest(APITestCase):
    @classmethod
    def tearDownClass(cls):
        Product.objects.all().delete()
        super().tearDownClass()

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.products = [Product.objects.create(name=f'Product #{i}',
                                               price=1000) for i in range(3)]
        for product in cls.products:
            product.save()
        cls.bb_1 = BlackBox.objects.create(name='Box 1', price=2000)
        amounts = [1, 1, 1]
        cls.items_1 = [BlackBoxItem.objects.create(
            black_box=cls.bb_1, product=product, amount=amount
        ) for product, amount in zip(cls.products, amounts)]
        for item in cls.items_1:
            item.save()
        cls.bb_1.save()

        cls.bb_2 = BlackBox.objects.create(name='Box 2', price=2000)
        amounts = [10, 20, 30]
        cls.items_2 = [BlackBoxItem.objects.create(
            black_box=cls.bb_2, product=product, amount=amount
        ) for product, amount in zip(cls.products, amounts)]
        for item in cls.items_2:
            item.save()
        cls.bb_2.save()

    def test_mock_open_small(self):
        res = self.bb_1.mock_open(3)
        self.assertEqual(set(res), set(self.bb_1.products()))
        res = self.bb_1.mock_open(0)
        self.assertEqual(res, [])

    def test_mock_open_large(self):
        res = self.bb_2.mock_open(60)
        self.assertEqual(Counter(res), Counter(
            {self.products[0]: 10, self.products[1]: 20, self.products[2]: 30}
        ))
        res = self.bb_2.mock_open(1000)
        self.assertEqual(Counter(res), Counter(
            {self.products[0]: 10, self.products[1]: 20, self.products[2]: 30}
        ))

    def test_api(self):
        pk = self.bb_1.pk
        response = self.client.post(reverse('blackbox-detail', args=[pk]) + 'mock_open/', data={'n': 10})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(set(data['product_names']), {f'Product #{i}' for i in range(3)})
