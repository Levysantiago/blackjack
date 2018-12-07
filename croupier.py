from player import Player
from deck import Deck
from card import Card
from itertools import cycle
from prettytable import PrettyTable


class Croupier:
    def __init__(self, fileConfig):
        dados = open(fileConfig, 'r')
        self.pedidoNovoJogo = None
        self.respostaPedido = True
        self.list_player = []
        self.deck = Deck()

        index = 0
        for line in dados:
            line = line.strip()
            ip, porta, nome = line.split(' ')
            self.list_player.append(Player(ip, porta, nome, index))
            index += 1
        dados.close()

    def getNext(self, playerID):
        player = self.findPlayer(playerID)
        tam = len(self.list_player) - 1
        index = player.getIndex()
        if(index == tam):
            return (self.list_player[0].ip, int(self.list_player[0].porta))
        else:
            index += 1
            return (self.list_player[index].ip, int(self.list_player[index].porta))

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
                  " com " + str(winner.getPoints()) + " pontos\n")

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

    def printHistorico(self, playerID):
        player = self.findPlayer(playerID)
        somador = 0
        table = PrettyTable()
        table.field_names = ["CARTA", "VALOR", "SOMATORIO"]
        for card in player.cards:
            somador += card.value()
            table.add_row([card.name(), card.value(), somador])
        print(table)
        print('\n')

    def showStatus(self, playerID):
        player = self.findPlayer(playerID)
        cardName, cardValue = player.getLastCard()

        print("\nSTATUS DO JOGO:")
        table = PrettyTable()
        table.field_names = ["JOGADORES", "STATUS"]
        msg_players = "\n"
        for p in self.list_player:
            if(p.isFinished()):
                table.add_row([p.getNome(), "Esperando"])
                msg_players += p.getNome() + " - Parou\n"
            else:
                table.add_row([p.getNome(), "Jogando"])
                msg_players += p.getNome() + " - Jogando\n"
        print(table)

        print("\nMEU STATUS:")
        table = PrettyTable()
        table.field_names = ["PONTOS", "ÚLTIMA CARTA", "VALOR"]
        if(cardName == None):
            cardName = ""
            cardValue = ""

        table.add_row([str(player.points), cardName, cardValue])
        print(table)
        print("\n")

    def pedirNovoJogo(self, playerID):
        self.pedidoNovoJogo = self.findPlayer(playerID)

    def desativarPedido(self):
        self.pedidoNovoJogo = None

    def temPedidoNovoJogo(self):
        if(self.pedidoNovoJogo != None):
            return True
        return False

    def printQuemPediuNovoJogo(self):
        print(self.pedidoNovoJogo.getNome() +
              " pediu para iniciar um novo jogo. Você aceita? (s/n)")

    def euPediNovoJogo(self, playerID):
        player = self.findPlayer(playerID)
        if(player.getIndex() == self.pedidoNovoJogo.getIndex()):
            return True
        return False

    def contabilizaRespostaPedido(self, resp):
        if(resp == 's'):
            self.respostaPedido = self.respostaPedido and True
        else:
            self.respostaPedido = self.respostaPedido and False

    def getRespostaPedido(self):
        return self.respostaPedido
