from player import Player
from deck import Deck
from card import Card
from itertools import cycle


class Croupier:
    def __init__(self, fileConfig):
        dados = open(fileConfig, 'r')
        self.list_player = []
        self.deck = Deck()

        index = 0
        for line in dados:
            line = line.strip()
            ip, porta, nome = line.split(' ')
            self.list_player.append(Player(ip, porta, nome, index))
            index += 1
        dados.close()
        self.pool = self.list_player

    def getNext(self, playerID):
        player = self.findPlayer(playerID)
        tam = len(self.list_player) - 1
        index = player.getIndex()
        if(index == tam):
            return (self.list_player[0].ip, int(self.list_player[0].porta))
        else:
            index += 1
            return (self.list_player[index].ip, int(self.list_player[index].porta))

    def showGameStatus(self):
        print("\nGAME STATUS:")
        for player in self.list_player:
            print("\nPlayer: "+player.getNome() +
                  "\nPoints = " + str(player.points))
        print("\n")

    def showResults(self):
        print("\nRESULTS:")
        winner = self.list_player[0]
        for player in self.list_player[1:]:
            points = player.getPoints()
            if(winner.getPoints() > 21):
                winner = player
            elif(points > winner.getPoints() and points <= 21):
                winner = player
        if(winner.getPoints() > 21):
            print("\nDraw\n")
        else:
            print("\nPlayer " + winner.getNome() +
                  " with " + str(winner.getPoints()) + " points\n")

    def findPlayer(self, playerID):
        return [x for x in self.list_player if x.ip == playerID][0]

    def getCard(self, playerID):
        self.deck.shuffle()
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
        msg_players = "\n"
        for p in self.list_player:
            if(p.isFinished()):
                msg_players += p.getNome() + " - Parou\n"
            else:
                msg_players += p.getNome() + " - Jogando\n"
        print("\nSTATUS:"
              "\nPoints = " + str(player.points) +
              msg_players)
        if(cardName != None):
            print("\nCard = "+cardName+" Value = "+str(cardValue))
        print("\n")
