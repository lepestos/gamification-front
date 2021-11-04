from math import floor, ceil
from typing import List, Dict


class LotteryUtil:
    def __init__(self, lots: List[Dict[str, int]],
                 write_off: float, referral_coeff: int, ticket_amount: int,
                 ticket_price: float):
        self.message = ''
        self.success = True
        self.lot_amounts = [lot['amount'] for lot in lots]
        self.lot_prices = [lot['price'] for lot in lots]
        self.write_off = write_off
        self.referral_coeff = referral_coeff
        self.set_ticket_amount(ticket_amount)
        self.total_cost = self.get_total_cost()
        self.set_ticket_price(ticket_price)
        self.min_profit = self.get_min_profit()
        self.min_rentability = self.get_min_rentability()
        self.max_rentability = self.get_max_rentability()

    def to_json(self):
        data = {
            'lots': [
                {'amount': amount, 'price': price}
                for amount, price in zip(self.lot_amounts, self.lot_prices)
            ],
            'write_off': self.write_off,
            'referral_coeff': self.referral_coeff,
            'ticket_amount': self.ticket_amount,
            'total_cost': self.total_cost,
            'ticket_price': self.ticket_price,
            'min_profit': self.min_profit,
            'min_rentability': round(self.min_rentability, 2),
            'max_rentability': round(self.max_rentability, 2),
            'success': self.success,
            'message': self.message
        }
        return data

    def set_ticket_amount(self, ticket_amount):
        if ticket_amount == 0:
            self.ticket_amount = self.get_ticket_amount()
        else:
            self.ticket_amount = ticket_amount

    def set_ticket_price(self, ticket_price):
        if ticket_price == 0:
            self.ticket_price = self.get_ticket_price()
        else:
            self.ticket_price = ticket_price
            self.write_off = self.get_write_off()

    def get_ticket_amount(self):
        return 4 * sum(self.lot_amounts)

    def get_total_cost(self):
        return sum(a * c for a, c in zip(self.lot_amounts, self.lot_prices))

    def get_ticket_price(self):
        return (self.write_off + self.total_cost) / self.ticket_amount

    def get_min_profit(self):
        return self.write_off - self.ticket_price * floor(self.ticket_amount / (self.referral_coeff + 1))

    def get_min_rentability(self):
        return self.min_profit / self.total_cost

    def get_max_rentability(self):
        return self.write_off / self.total_cost

    def get_write_off(self):
        return self.ticket_amount * self.ticket_price - self.total_cost


if __name__ == '__main__':
    input_data = {
        'lots': [
            {'amount': 1, 'price': 1000},
            {'amount': 2, 'price': 500},
            {'amount': 3, 'price': 200},
        ],
        'write_off': 1000,
        'referral_coeff': 4,
        'ticket_amount': 0,
        'ticket_price': 0
    }
    lottery = LotteryUtil(**input_data)
    print(lottery.to_json())

    input_data = {
        'lots': [
            {'amount': 1, 'price': 1000},
            {'amount': 2, 'price': 500},
            {'amount': 3, 'price': 200},
        ],
        'write_off': 1000,
        'referral_coeff': 4,
        'ticket_amount': 30,
        'ticket_price': 130
    }
    lottery = LotteryUtil(**input_data)
    print(lottery.to_json())
