import socket
import threading
import os
import random
import pickle
import time
#AGREGAR CAMBIO MENSAJE MINUSCULAS

HEADER = 1024
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER,PORT)
FORMAT = 'utf8'
#DISCONNECT_MESSAGE = "DISCONNECT"

def all_hosts():
    os.system("cls")
    for client in clients_list:
        print(client)

def broadcast_msg(name,msg,newindex):
    if newindex == -1:
        for client in clients_list:
            client.send(str(msg).encode(FORMAT))
    elif newindex == -2:
        for client in clients_list:
            client.send(msg)


def handle_client(conn,addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    start_game = False
    connected = True
    global indexchoice
    while connected:
        msg = conn.recv(HEADER).decode(FORMAT).strip()
        
        if start_game:
            #El juego comienza
            if msg == correct_answers[indexchoice]:
                print("Respuesta correcta ",msg)
                
                if correct_answers.index(msg):
                    indexes.remove(correct_answers.index(msg))
                if indexes:
                    indexchoice = random.choice(indexes)
                
                broadcast_msg("","i"+str(clients_addr.index(addr))+str(indexchoice),-1)
                
            else:
                conn.send("w".encode(FORMAT))
            
        #Si el juego comenzo
        else:
            if msg == "r":
                print("preparado")
                print(clients_ready)
                clients_ready[clients_addr.index(addr)] = 1     
                    
            if sum(clients_ready) == threading.active_count() - 1:
                start_game = True
                broadcast_msg("","r",-1)
                #conn.send("r".encode(FORMAT))
                time.sleep(0.5)
                broadcast_msg("",str(indexchoice),-1)
                time.sleep(0.5)
                broadcast_msg("",pickle.dumps(clients_addr),-2)
                print("comenzo el juego")
            else:
                print("Faltan jugadores preparados")            
            
        #print(f"[{addr}] {msg}")
        '''
        except:
            if conn in clients_list:
                print(clients_ready, " ",clients_list.index(conn)," ",clients_list)
                clients_ready.pop(clients_list.index(conn))
                clients_list.remove(conn)
                clients_addr.remove(addr)
                
                print(addr," Removido")  
            '''
    print("Conexion cerrada")
    conn.close()
    
def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        
        clients_list.append(conn)
        clients_addr.append(addr)
        clients_ready.append(0)
        print(len(clients_list))
        thread = threading.Thread(target=handle_client, args=(conn,addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1 }")

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

clients_list = []
clients_addr = []
clients_ready = []

turno = 0

correct_answers = []
listImgsPath = []

for i in  os.listdir(path="./images"):
    listImgsPath.append(i)
    correct_answers.append(i[:-4])
indexes = [*range(0,len(listImgsPath),1)]

puntajeNum = 10

indexchoice = random.choice(indexes)
print("Servidor iniciado...")
print("Respuestas correctas:")
print(correct_answers)
print("actual correcta:",correct_answers[indexchoice])

start()

#https://www.youtube.com/watch?v=3QiPPX-KeSc
#https://www.youtube.com/watch?v=lGL1XZfix-w