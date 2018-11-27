from player import Player
from deck import Deck
from card import Card
from itertools import cycle


class Croupier:

    def __init__(self, fileConfig):
        dados = open(fileConfig, 'r')
        self.list_player = []
        self.deck = Deck()

        for line in dados:
            line = line.strip()
            ip, porta, nome = line.split(' ')
            self.list_player.append(Player(ip, porta, nome))
        self.pool = self.list_player
        #next(self.pool)
    
    def getNext(self):
        return self.list_player[1].ip, self.list_player[1].porta
    '''
    def getNext(self):
        return next(self.pool).ip, next(self.pool).porta
    '''

    def showGameStatus():
        pass

    def findPlayer(self, playerID):
        return [x for x in self.list_player if x.ip == playerID][0]

    def getCard(self, playerID):
        player = self.findPlayer(playerID)
        if (not player.isFinish()):
            if (not self.deck.empty()):
                player.newCard(self.deck.pop())
                self.showPlayer(player)

        if (self.allFinished()):
            self.showResults()

    def finish(self, playerID):
        for player in self.list_player:
            if (player.ip == playerID):
                player.setFinished(True)

    def allFinished(self):
        for player in self.list_player:
            if (not player.finished):
                return False
        return True

    def showPlayer(self, player):
        print("Points = " + str(player.points) +
              "\nFinished = " + str(player.isFinish()) +
              "\nCard = "+str(player.lastCard[0])+" Value = "+str(player.lastCard[1]))

def main():
    cr = Croupier("conf.txt")
    #print(cr.findPlayer("192.168.0.212")[0].nome)


main()
