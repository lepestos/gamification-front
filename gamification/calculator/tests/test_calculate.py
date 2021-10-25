from copy import deepcopy

from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status


class CalculateTest(APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.data = {
            'lot_cost': {'costly': 1000, 'middle': 300, 'cheap': 100},
            'costly_amount': 100,
            'rentability': 0.2,
            'loyalty': 0.6,
            'black_box_cost': 0
        }
        cls.data2 = deepcopy(cls.data)
        cls.data2['black_box_cost'] = 400
        cls.data3 = deepcopy(cls.data)
        cls.data3['black_box_cost'] = 100

    def test_calculate(self):
        response = self.client.post(reverse('blackbox-list') + 'calculate/', data=self.data, format='json')
        exp_amounts = {'costly': 100, 'middle': 171, 'cheap': 181}
        exp_probabilities = {'costly': 0.222, 'middle': 0.378, 'cheap': 0.4}
        exp_cur, exp_max, exp_min = 460, 768, 264
        self.assert_response_is_correct(response,  exp_amounts, exp_probabilities, exp_cur, exp_max, exp_min)
        self.assertEqual(response.data['message'], '')

    def test_calculate_with_given_good_price(self):
        response = self.client.post(reverse('blackbox-list') + 'calculate/', data=self.data2, format='json')
        exp_amounts = {'costly': 100, 'middle': 271, 'cheap': 248}
        exp_probabilities = {
            'costly': 0.162,
            'middle': 0.439,
            'cheap': 0.4
        }
        exp_cur, exp_max, exp_min = 400, 768, 264
        self.assert_response_is_correct(response, exp_amounts, exp_probabilities, exp_cur, exp_max, exp_min)
        self.assertEqual(response.data['message'], '')

    def test_calculate_with_given_bad_price(self):
        response = self.client.post(reverse('blackbox-list') + 'calculate/', data=self.data3, format='json')
        exp_amounts = {'costly': 100, 'middle': 171, 'cheap': 181}
        exp_probabilities = {'costly': 0.222, 'middle': 0.378, 'cheap': 0.4}
        exp_cur, exp_max, exp_min = 460, 768, 264
        self.assert_response_is_correct(response,  exp_amounts, exp_probabilities, exp_cur, exp_max, exp_min)
        self.assertEqual(response.data['message'], f'Цена должна лежать в интервале от 270 до 760.')

    def assert_response_is_correct(self, response, exp_amounts, exp_probabilities, exp_cur, exp_max, exp_min):
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['amounts'], exp_amounts)
        for key in exp_probabilities:
            self.assertLess(abs(response.data['probabilities'][key] - exp_probabilities[key]), 1e-2)
        self.assertEqual(response.data['black_box_cost']['cur'], exp_cur)
        self.assertEqual(response.data['black_box_cost']['max'], exp_max)
        self.assertEqual(response.data['black_box_cost']['min'], exp_min)
