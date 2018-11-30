from player import Player
from deck import Deck
from card import Card
from itertools import cycle


class Croupier:
    def __init__(self, fileConfig):
        dados = open(fileConfig, 'r')
        self.list_player = []
        self.deck = Deck()
        self.playerIndex = 0

        for line in dados:
            line = line.strip()
            ip, porta, nome = line.split(' ')
            self.list_player.append(Player(ip, porta, nome))
        self.pool = self.list_player

    def getNext(self):
        tam = len(self.list_player) - 1
        if(self.playerIndex == tam):
            self.playerIndex = 0
        self.playerIndex += 1
        return self.list_player[self.playerIndex].ip, self.list_player[self.playerIndex].porta

    def showGameStatus(self):
        print("\nGAME STATUS:")
        for player in self.list_player:
            print("\nPlayer: "+player.getNome() +
                  "\nPoints = " + str(player.points))
        print("\n")

    def findPlayer(self, playerID):
        return [x for x in self.list_player if x.ip == playerID][0]

    def getCard(self, playerID):
        player = self.findPlayer(playerID)
        if (not player.isFinished()):
            if (not self.deck.empty()):
                card = player.newCard(self.deck.pop())
            return card.name()

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

    def showPlayerStatus(self, playerID):
        player = self.findPlayer(playerID)
        cardName, cardValue = player.getLastCard()
        print("\nSTATUS:"
              "\nPoints = " + str(player.points) +
              "\nFinished = " + str(player.isFinished()) +
              "\nCard = "+cardName+" Value = "+str(cardValue)+"\n")
