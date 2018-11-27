
class Player():

    def __init__(self, ip, porta, nome):
        self.ip = ip
        self.nome = nome
        self.porta = porta
        self.finished = False
        self.points = 0
        self.lastCard = ()

    def isFinish(self):
        return self.finished

    def newCard(self, card):
        self.lastCard = (card.name(), card.value())
        self.points += card.value()
        if (self.points > 21):
            self.finished = True

    def setFinished(self, valor):
        self.finished = valor
