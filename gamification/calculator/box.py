from math import sqrt, ceil
from typing import List


PROFIT= 0.15
LOYALTY = 0.60


class Box:
    def __init__(self, prices: List[float],  max_count_costly: float,
                 profit: float=PROFIT, loyalty: float=LOYALTY):
        self.prices = [float(price) for price in prices]
        self.max_count_costly = max_count_costly
        self.profit = float(profit)
        self.loyalty = float(loyalty)
        self.ticket_price = round(sqrt(self.get_max_ticket_price() * self.get_min_ticket_price()), 2)
        self.probabilities = self.get_probabilities()
        self.amounts = self.get_amounts()

    def get_probabilities(self):
        p3 = 1 - self.loyalty
        p1 = (self.ticket_price * (1 - self.profit) -
              LOYALTY * (self.prices[1] - self.prices[2]) - self.prices[2]) \
             / (self.prices[0] - self.prices[1])
        p2 = self.loyalty - p1
        return p1, p2, p3

    def get_max_ticket_price(self):
        return (self.loyalty * self.prices[0] + (1 - self.loyalty) * self.prices[2]) / (1 - self.profit)

    def get_min_ticket_price(self):
        return (self.loyalty * self.prices[1] + (1 - self.loyalty) * self.prices[2]) / (1 - self.profit)

    def get_amounts(self):
        a1 = self.max_count_costly
        p1, p2, p3 = self.probabilities
        return a1, ceil(a1 * p2 / p1), ceil(a1 * p3 / p1)

if __name__ == '__main__':
    box = Box([50, 30, 20], 10, 0.1, 0.7)
    print(box.get_amounts())
    print(box.ticket_price)