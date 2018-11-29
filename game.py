import socket
from croupier import Croupier
import pickle

IP = '192.168.137.160'
port = 5101
buffer_size = 1024

def get_menu():
    menu = '(0) - Novo Jogo \n'
    menu += '(1) - Carta \n' 
    menu += '(2) - Sem mais cartas \n' 
    menu += '(3) - Proximo \n' 

    return menu

def next (ip, porta, croupier):
    player = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    player.connect((ip,porta))

    croupier_dump = pickle.dumps(croupier)
    player.send(croupier_dump)
    player.close()

def waitMyTurn():
    player = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    player.bind((IP, port))
    player.listen(1)
    conexao, endereco = player.accept()

    while True:
        croupier = conexao.recv(2024)
    return pickle.loads(croupier)

def playFirst(ip):
    file = open("conf.txt", "r")
    ret = file.readline().split(' ')[0] == IP
    file.close()
    return ret

def main():
    croupier = None
    flag = False
    if(playFirst(IP)):
        croupier = Croupier("conf.txt")
        flag = True

    if(not flag):
        croupier = waitMyTurn()
        flag = True

    while(not croupier.deck.empty()):
        print(get_menu())
        option = raw_input()
        if(option == '0'):
            print("Novo Jogo")
        elif(option == '1'):
            croupier.getCard(IP)
        elif(option == '2'):
            print("Sem mais cartas")
        elif(option == '3'):
            print("Proximo")
            ip, porta = croupier.getNext()
            print("enviando")
            next(ip, int(porta), croupier)
            print("enviou")
            flag = False

        if(not flag):
            croupier = waitMyTurn()
            flag = True
        

if __name__ == "__main__":
    main()