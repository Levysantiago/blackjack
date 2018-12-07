from croupier import Croupier
import socket
import pickle
import os

os.system('clear')
IP = '192.168.2.59'
PORT = 5101
buffer_size = 4096


def get_menu():
    menu = '(0) - Novo Jogo \n'
    menu += '(1) - Carta \n'
    menu += '(2) - Sem mais cartas \n'
    menu += '(3) - Proximo \n'
    menu += '(4) - Status Jogo\n'
    menu += '(5) - Meu Historico \n'

    return menu


def next(croupier):
    player = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    nextPlayer = croupier.getNext(IP)
    player.connect(nextPlayer)

    croupier_dump = pickle.dumps(croupier)
    player.send(croupier_dump)
    player.close()


def waitMyTurn():
    player = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    player.bind((IP, PORT))
    player.listen(1)
    conexao, endereco = player.accept()

    while True:
        dados = conexao.recv(buffer_size)
        if(dados != 0):
            break
    player.close()
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
        envioFinal = 0

        while(croupier.temPedidoNovoJogo()):
            os.system("clear")
            # Se foi eu que fiz o pedido
            if(croupier.euPediNovoJogo(IP)):
                if(croupier.getRespostaPedido()):
                    os.system("clear")
                    del croupier
                    croupier = Croupier("conf.txt")
                    jogando = True
                else:
                    print("\nA inicialização de um novo jogo nao foi aceita.\n")
                    croupier.desativarPedido()
                    # break
            # Se não foi eu que fiz o pedido
            else:
                croupier.printQuemPediuNovoJogo()
                option = input()
                croupier.contabilizaRespostaPedido(option)
                jogando = False
                os.system("clear")
                next(croupier)
                print("Espere sua vez de jogar...")
                croupier = waitMyTurn()
                jogando = True
                os.system("clear")

        print(get_menu())
        option = input()
        os.system("clear")

        if(option == '0'):
            croupier.pedirNovoJogo(IP)
            next(croupier)
            jogando = False
        elif(option == '1'):
            croupier.getCard(IP)
            croupier.showStatus(IP)
        elif(option == '2'):
            croupier.finish(IP)
            croupier.showStatus(IP)
        elif(option == '3'):
            next(croupier)
            jogando = False
        elif(option == '4'):
            croupier.showStatus(IP)
        elif(option == '5'):
            croupier.printHistorico(IP)

        if(not jogando):
            print("Espere sua vez de jogar...")
            croupier = waitMyTurn()
            jogando = True
            os.system("clear")

        while(croupier.allFinished()):
            jogando = False
            os.system("clear")
            croupier.showResults()

            if(envioFinal > 0):
                # Ultimo a receber a mensagem
                del croupier
                croupier = Croupier("conf.txt")
                jogando = True
            else:
                next(croupier)
                envioFinal += 1

            if(not jogando):
                print("Espere sua vez de jogar...")
                croupier = waitMyTurn()
                jogando = True
                os.system("clear")


if __name__ == "__main__":
    main()
