from croupier import Croupier
import socket
import pickle
import os

os.system('clear')
IP = '192.168.2.59'
PORT = 5101
buffer_size = 1024


def get_menu():
    menu = '(0) - Novo Jogo \n'
    menu += '(1) - Carta \n'
    menu += '(2) - Sem mais cartas \n'
    menu += '(3) - Proximo \n'

    return menu


def next(ip, porta, croupier):
    player = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    player.connect((ip, porta))

    croupier_dump = pickle.dumps(croupier)
    player.send(croupier_dump)
    player.close()


def waitMyTurn():
    player = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    player.bind((IP, PORT))
    player.listen(1)
    conexao, endereco = player.accept()

    while True:
        dados = conexao.recv(4096)
        if(dados != 0):
            break
    return pickle.loads(dados)


def playFirst(ip):
    file = open("conf.txt", "r")
    ret = file.readline().split(' ')[0] == IP
    file.close()
    return ret


def main():
    croupier = None
    jogando = False
    if(playFirst(IP)):
        croupier = Croupier("conf.txt")
        jogando = True

    if(not jogando):
        croupier = waitMyTurn()
        jogando = True

    while(not croupier.deck.empty()):
        print(get_menu())
        if(croupier.allFinished()):
            break
        option = raw_input()
        if(option == '0'):
            print("Novo Jogo")
        elif(option == '1'):
            os.system('clear')
            croupier.getCard(IP)
            croupier.showPlayerStatus(IP)
        elif(option == '2'):
            croupier.finish(IP)
            os.system('clear')
            croupier.showPlayerStatus(IP)
        elif(option == '3'):
            ip, porta = croupier.getNext()
            next(ip, int(porta), croupier)
            jogando = False
            os.system('clear')

        if(croupier.allFinished()):
            break
        elif(not jogando):
            croupier = waitMyTurn()
            jogando = True
    ip, porta = croupier.getNext()
    try:
        next(ip, int(porta), croupier)
    except:
        pass  # Todos receberam
    os.system("clear")
    croupier.showResults()


if __name__ == "__main__":
    main()
