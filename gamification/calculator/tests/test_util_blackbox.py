import unittest

from calculator.utils.box import Box


class BlackBoxTest(unittest.TestCase):
    def test_0_probability_costly(self):
        data = {
            "lot_cost": {'costly': 400, 'middle': 200, 'cheap': 100},
            "costly_amount": 10,
            "black_box_cost": 160,
            "rentability": 0,
            "loyalty": 0.6
        }
        box = Box(**data)
        res = box.to_json()
        self.assertEqual(res['amounts'], {'costly': 0, 'middle': 10, 'cheap': 7})
