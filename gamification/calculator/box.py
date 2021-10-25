from math import sqrt, ceil, floor
from typing import Dict, List


PROFIT= 0.15
LOYALTY = 0.6


class Box:
    def __init__(self, lot_cost: Dict[str, float],  costly_amount: int,
                 black_box_cost: float, rentability: float=PROFIT,
                 loyalty: float=LOYALTY):
        self.prices = [float(lot_cost[category]) for category in ['costly', 'middle', 'cheap']]
        self.max_count_costly = costly_amount
        self.profit = float(rentability)
        self.loyalty = float(loyalty)
        self.set_ticket_price(black_box_cost)
        self.probabilities = self.get_probabilities()
        self.amounts = self.get_amounts()

    def set_ticket_price(self, black_box_cost):
        max_price = self.get_max_ticket_price()
        min_price = self.get_min_ticket_price()
        if black_box_cost == 0 or black_box_cost < min_price or black_box_cost > max_price:
            self.ticket_price = round(sqrt(self.get_max_ticket_price() * self.get_min_ticket_price()), 2)
            if black_box_cost == 0:
                self.message = ''
            else:
                self.message = f'Цена должна лежать в интервале от ' \
                               f'{ceil(min_price / 10) * 10} до {floor(max_price / 10) * 10}.'
        else:
            self.ticket_price = float(black_box_cost)
            self.message = ''

    def get_probabilities(self):
        p3 = 1 - self.loyalty
        p1 = (self.ticket_price / (self.profit + 1)
              - self.loyalty * (self.prices[1] - self.prices[2])
              - self.prices[2])\
             / (self.prices[0] - self.prices[1])
        p2 = self.loyalty - p1
        return p1, p2, p3

    def get_max_ticket_price(self):
        return round((self.profit + 1)
                     * (self.loyalty * self.prices[0]
                        - self.loyalty * self.prices[2] + self.prices[2]),
                     2)

    def get_min_ticket_price(self):
        return round((self.profit + 1)
                     * (self.loyalty * self.prices[1]
                        - self.loyalty * self.prices[2] + self.prices[2]),
                     2)

    def get_amounts(self):
        a1 = self.max_count_costly
        p1, p2, p3 = self.probabilities
        return a1, ceil(a1 * p2 / p1), ceil(a1 * p3 / p1)

    def get_rounded_ticket_price(self):
        return ceil(self.ticket_price / 10) * 10


def convert_to_dict(lst: List) -> Dict:
    return {key: round(value, 3) for key, value in zip(['costly', 'middle', 'cheap'], lst)}


if __name__ == '__main__':
    prices = {
        'costly': 1000,
        'middle': 300,
        'cheap': 100,
    }
    b = Box(prices, costly_amount=100, black_box_cost=0, rentability=0.2, loyalty=0.6)
    print(b.probabilities)
    print(b.amounts)
    print(b.ticket_price)
    print(b.get_min_ticket_price())
    print(b.get_max_ticket_price())