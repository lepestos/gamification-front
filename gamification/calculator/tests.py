from copy import deepcopy
from collections import Counter

from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from .models import Product, BlackBox, BlackBoxItem


class ProductTest(APITestCase):
    def tearDown(self):
        Product.objects.all().delete()

    def test_post(self):
        data = {
            'name': 'bicycle',
            'price': 1000
        }
        response = self.client.post(reverse('product-list'), data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 1)
        p = Product.objects.all()[0]
        self.assertEqual(p.name, 'bicycle')
        self.assertEqual(p.price, 1000)

    def test_delete(self):
        data = {
            'name': 'product1',
            'price': 999
        }
        response = self.client.post(reverse('product-list'), data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        pk = Product.objects.get(name='product1').pk
        response = self.client.delete(reverse('product-detail', args = [pk]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        with self.assertRaises(Product.DoesNotExist):
            Product.objects.get(pk=pk)

    def test_get(self):
        data  = {
            'name': 'product2',
            'price': 902
        }
        response = self.client.post(reverse('product-list'), data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        pk = Product.objects.get(name='product2').pk
        response = self.client.get(reverse('product-detail', args=[pk]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['name'], 'product2')
        self.assertEqual(response.json()['price'], 902)


class BlackBoxTest(APITestCase):
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
        pks = [product.pk for product in cls.products]
        cls.data = {
            'name': 'Box',
            'products': pks,
            'amounts': [10, 30, 70],
            'price': 2000
        }
        cls.amounts = {
            f'Product #{i}': amount for i, amount in zip(range(3), [10, 30, 70])
        }

    def tearDown(self):
        BlackBox.objects.all().delete()
        BlackBoxItem.objects.all().delete()

    def test_post(self):
        response = self.client.post(reverse('blackbox-list'), data=self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        bb = BlackBox.objects.get(name='Box')
        for item in bb.items.all():
            self.assertEqual(item.amount, self.amounts[item.product.name])
        self.assertEqual(bb.price, 2000)

    def test_delete(self):
        response = self.client.post(reverse('blackbox-list'), data=self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        pk = BlackBox.objects.get(name='Box').pk
        response = self.client.delete(reverse('blackbox-detail', args=[pk]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        with self.assertRaises(BlackBox.DoesNotExist):
            BlackBox.objects.get(name='Box')

    def test_get(self):
        response = self.client.post(reverse('blackbox-list'), data=self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        pk = BlackBox.objects.get(name='Box').pk
        response = self.client.get(reverse('blackbox-detail', args=[pk]))
        data = response.json()
        self.assertEqual({item['product']['name'] for item in data['items']},
                         {f'Product #{i}' for i in range(3)})
        self.assertEqual(data['price'], 2000)

    def test_put(self):
        self.client.post(reverse('blackbox-list'), data=self.data)
        pk = BlackBox.objects.get(name='Box').pk
        new_data = deepcopy(self.data)
        new_data['name'] = 'Another Box'
        other_products = [Product.objects.create(name=f'Another product #{i}',
                                                 price=2000) for i in range(3)]
        for product in other_products:
            product.save()
        pks = [product.pk for product in other_products]
        new_data['products'] = pks
        other_amounts = {
            f'Another product #{i}': prob for i, prob in zip(range(3), [10, 30, 70])
        }
        response = self.client.put(reverse('blackbox-detail', args=[pk]), data=new_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        bb = BlackBox.objects.get(pk=pk)
        self.assertEqual(bb.name, 'Another Box')
        for item in bb.items.all():
            self.assertEqual(item.amount, other_amounts[item.product.name])
            self.assertEqual(item.product.price, 2000)
        self.assertEqual(BlackBox.objects.count(), 1)
        self.assertEqual(BlackBoxItem.objects.count(), 3)
        self.assertEqual(bb.price, 2000)


class CalculateTest(APITestCase):
    def test_calculate(self):
        data = {
            'lot_cost': {
                'costly': 100,
                'middle': 50,
                'cheap': 20
            },
            'costly_amount': 10,
            'rentability': 0.2,
            'loyalty': 0.6,
            'black_box_cost': 0
        }
        response = self.client.post(reverse('blackbox-list') + 'calculate/', data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        exp_amounts = {
            'costly': 10,
            'middle': 14,
            'cheap': 16
        }
        exp_probabilities = {
            'costly': 0.257,
            'middle': 0.343,
            'cheap': 0.4
        }
        self.assertEqual(response.data['amounts'], exp_amounts)
        for key in exp_probabilities:
            self.assertLess(abs(response.data['probabilities'][key] - exp_probabilities[key]), 1e-2)
        self.assertEqual(response.data['black_box_cost']['cur'], 61.0)
        self.assertEqual(response.data['black_box_cost']['max'], 81.6)
        self.assertEqual(response.data['black_box_cost']['min'], 45.6)

        data['black_box_cost'] = 50
        response = self.client.post(reverse('blackbox-list') + 'calculate/', data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        exp_amounts = {
            'costly': 10,
            'middle': 72,
            'cheap': 55
        }
        exp_probabilities = {
            'costly': 0.073,
            'middle': 0.527,
            'cheap': 0.4
        }
        self.assertEqual(response.data['amounts'], exp_amounts)
        for key in exp_probabilities:
            self.assertLess(abs(response.data['probabilities'][key] - exp_probabilities[key]), 1e-2)
        self.assertEqual(response.data['black_box_cost']['cur'], 50)
        self.assertEqual(response.data['black_box_cost']['max'], 81.6)
        self.assertEqual(response.data['black_box_cost']['min'], 45.6)


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
