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

        cls.bb_1 = cls.create_bb('Box 1', 2000, cls.products, [1, 1, 1])
        cls.bb_2 = cls.create_bb('Box 2', 2000, cls.products, [10, 20, 30])

    @staticmethod
    def create_bb(name, price, products, amounts):
        bb = BlackBox.objects.create(name=name, price=price, loyalty=0.6, rentability=0.3)
        items = [BlackBoxItem.objects.create(
            black_box=bb, product=product, amount=amount
        ) for product, amount in zip(products, amounts)]
        for item in items:
            item.save()
        bb.save()
        return bb

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
