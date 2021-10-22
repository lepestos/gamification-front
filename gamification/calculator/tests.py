from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from .models import Product, BlackBox


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
            'amount': [10, 30, 70]
        }
        cls.amounts = {
            f'Product #{i}': amount for i, amount in zip(range(3), [10,30,70])
        }

    def tearDown(self):
        BlackBox.objects.all().delete()

    def test_post(self):
        response = self.client.post(reverse('blackbox-list'), data=self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        bb = BlackBox.objects.get(name='Box')
        for item in bb.items.all():
            self.assertEqual(item.amount, self.amounts[item.product.name])

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


class CalculateTest(APITestCase):
    def test_calculate(self):
        data = {
            'prices': [50, 30, 20],
            'max_count_costly': 10,
            'profit': 0.1,
            'loyalty': 0.7,
        }
        response = self.client.post(reverse('blackbox-list') + 'calculate/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(list(response.data['amounts']), [10, 10, 9])
