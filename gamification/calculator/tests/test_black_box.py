from copy import deepcopy

from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from calculator.models import Product, BlackBox, BlackBoxItem


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
