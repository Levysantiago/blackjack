from random import shuffle
from card import Card


class Deck:
    cards = [Card('AD', 1), Card('AC', 1), Card('AS', 1), Card('AH', 1),
             Card('2D', 2), Card('2C', 2), Card('2S', 2), Card('2H', 2),
             Card('3D', 3), Card('3C', 3), Card('3S', 3), Card('3H', 3),
             Card('4D', 4), Card('4C', 4), Card('4S', 4), Card('4H', 4),
             Card('5D', 5), Card('5C', 5), Card('5S', 5), Card('5H', 5),
             Card('6D', 6), Card('6C', 6), Card('6S', 6), Card('6H', 6),
             Card('7D', 7), Card('7C', 7), Card('7S', 7), Card('7H', 7),
             Card('8D', 8), Card('8C', 8), Card('8S', 8), Card('8H', 8),
             Card('9D', 9), Card('9C', 9), Card('9S', 9), Card('9H', 9),
             Card('10D', 10), Card('10H', 10), Card('10S', 10), Card('10H', 10),
             Card('JD', 10), Card('JH', 10), Card('JS', 10), Card('JH', 10),
             Card('QD', 10), Card('QH', 10), Card('QS', 10), Card('QH', 10),
             Card('KD', 10), Card('KH', 10), Card('KS', 10), Card('KH', 10)]

    def __init__(self):
        shuffle(self.cards)

    def pop(self):
        return self.cards.pop()

    def empty(self):
        return not self.cards