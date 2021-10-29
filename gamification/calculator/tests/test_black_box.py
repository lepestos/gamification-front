from copy import deepcopy
from decimal import Decimal

from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from calculator.models import Product, BlackBox, BlackBoxItem
from calculator.utils.box import convert_to_list


class BlackBoxTest(APITestCase):
    @classmethod
    def tearDownClass(cls):
        Product.objects.all().delete()
        super().tearDownClass()

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.data = {
            'name': 'Box',
            'price': 200,
            'lot_cost': {'costly': 1000, 'middle': 100, 'cheap': 10},
            'lot_amount': {'costly': 1, 'middle': 3, 'cheap': 6},
        }
        cls.other_data = {
            'name': 'Box',
            'price': 40,
            'lot_cost': {'costly': 100, 'middle': 10, 'cheap': 1},
            'lot_amount': {'costly': 2, 'middle': 3, 'cheap': 5},
        }

    def tearDown(self):
        BlackBox.objects.all().delete()
        BlackBoxItem.objects.all().delete()

    def test_post(self):
        response = self.client.post(reverse('blackbox-list'), data=self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        bb = BlackBox.objects.get(name='Box')
        self.assertEqual(convert_to_list(bb.lot_cost()), [1000, 100, 10])
        self.assertEqual(convert_to_list(bb.lot_amount()), [1, 3, 6])
        self.assertEqual(bb.price, 200)
        self.assertEqual(bb.loyalty, Decimal('0.4'))
        self.assertEqual(bb.rentability, Decimal('0.47'))

    def test_delete(self):
        response = self.client.post(reverse('blackbox-list'), data=self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        pk = BlackBox.objects.get(name='Box').pk
        response = self.client.delete(reverse('blackbox-detail', args=[pk]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        with self.assertRaises(BlackBox.DoesNotExist):
            BlackBox.objects.get(name='Box')

    def test_get(self):
        response = self.client.post(reverse('blackbox-list'), data=self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        pk = BlackBox.objects.get(name='Box').pk
        response = self.client.get(reverse('blackbox-detail', args=[pk]))
        data = response.json()
        self.assertEqual(data['name'], 'Box')
        self.assertEqual(data['price'], 200)
        self.assertEqual(data['lot_cost'], {'costly': 1000, 'middle': 100, 'cheap': 10})
        self.assertEqual(data['lot_amount'], {'costly': 1, 'middle': 3, 'cheap': 6})
        self.assertEqual(data['loyalty'], 0.4)
        self.assertEqual(data['rentability'], 0.47)
        self.assertEqual(data['max_count_costly'], 1)

    def test_put(self):
        self.client.post(reverse('blackbox-list'), data=self.data, format='json')
        pk = BlackBox.objects.get(name='Box').pk
        response = self.client.put(reverse('blackbox-detail', args=[pk]),
                                   data=self.other_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        bb = BlackBox.objects.get(pk=pk)
        self.assertEqual(convert_to_list(bb.lot_cost()), [100, 10, 1])
        self.assertEqual(convert_to_list(bb.lot_amount()), [2, 3, 5])
        self.assertEqual(bb.price, 40)
        self.assertEqual(bb.loyalty, Decimal('0.5'))
        self.assertEqual(bb.rentability, Decimal('0.70'))
        self.assertEqual(BlackBoxItem.objects.all().count(), 3)
