
class Player():

    def __init__(self, ip, porta, nome, index):
        self.index = index
        self.ip = ip
        self.nome = nome
        self.porta = porta
        self.finished = False
        self.points = 0
        self.cards = []

    def isFinished(self):
        return self.finished

    def newCard(self, card):
        self.cards.append(card)
        self.points += card.value()
        if (self.points > 21):
            self.finished = True
        return card

    def getLastCard(self):
        try:
            return self.cards[-1].name(), self.cards[-1].value()
        except:
            return None, None

    def setFinished(self, valor):
        self.finished = valor

    def getNome(self):
        return self.nome

    def getPoints(self):
        return self.points

    def getIndex(self):
        return self.index
