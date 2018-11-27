import socket
from croupier import Croupier
import pickle

IP = '10.42.0.159'
port = 5101
buffer_size = 1024
player = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
player.bind((IP, port))

def get_menu():
    menu = '(0) - Novo Jogo \n'
    menu += '(1) - Carta \n' 
    menu += '(2) - Sem mais cartas \n' 
    menu += '(3) - Proximo \n' 

    return menu


def receive (conexao, endereco):
    while conexao != None:
        msg = conexao.recv(buffer_size)
        croupier = pickle.loads(msg)
        conexao.close()
        conexao = None
    return croupier

def next (ip, porta, croupier):
    player.connect((ip,porta))
    croupier_dump = pickle.dumps(croupier)
    player.send(croupier_dump)

def waitMyTurn():
    conexao = None
    player.listen(5)
    while conexao == None:
        conexao,endereco = player.accept()
    return conexao, endereco

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
        conexao, endereco = waitMyTurn()
        receive(conexao, endereco)
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
            #croupier = None
            #receive(conexao, endereco)
            
        if(not flag):
            conexao, endereco = waitMyTurn()
            receive(conexao, endereco)
            flag = True
        

if __name__ == "__main__":
    main()