import unittest
from random import seed, randint

from calculator.utils.lottery import Lottery


seed(42)

class LotteryTest(unittest.TestCase):
    def test_initial_input(self):
        for _ in range(10):
            input_data = {
                'lots': [
                    {'price': randint(100, 1000), 'amount': randint(1,10)} for _ in range(3)
                ],
                'write_off': randint(1000, 20000),
                'referral_coeff': randint(1, 10),
                'ticket_amount': 0,
                'ticket_price': 0
            }
            lottery = Lottery(**input_data)
            res = lottery.to_json()
            self.assertGreater(res['ticket_price'], 0)
            self.assertGreater(res['ticket_amount'], 0)
            self.assertGreater(res['total_cost'], 0)

    def test_recalculate(self):
        for _ in range(10):
            input_data = {
                'lots': [
                    {'price': randint(100, 1000), 'amount': randint(1,10)} for _ in range(3)
                ],
                'write_off': 0,
                'referral_coeff': randint(1, 10),
                'ticket_amount': randint(30, 1000),
                'ticket_price': randint(100, 1000),
            }
            lottery = Lottery(**input_data)
            res = lottery.to_json()
            self.assertGreater(res['total_cost'], 0)
