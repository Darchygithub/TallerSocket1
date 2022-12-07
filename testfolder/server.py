import socket
import threading
import os
import random
import pickle
import time

HEADER = 1024
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER,PORT)
FORMAT = 'utf8'

#Funcion que muestra todos los host actualmente conectados
def all_hosts():
    os.system("cls")
    for client in clients_list:
        print(client)

#Funcion que envia un mensaje codificado o no codificado a todos los clientes
def broadcast_msg(msg,newindex):
    if newindex == -1:
        for client in clients_list:
            client.send(str(msg).encode(FORMAT))
    elif newindex == -2:
        for client in clients_list:
            client.send(msg)

#Funcion que maneja la conexión de cada cliente en específico
def handle_client(conn,addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    start_game = False
    connected = True
    global indexchoice
    while connected:
        msg = conn.recv(HEADER).decode(FORMAT).strip()
        
        #Condición que detecta si el juego comenzó o no
        if start_game:            
            msg = msg.lower()
            if msg == correct_answers[indexchoice]:
                print("Respuesta correcta ",msg)                    
                
                indexes.remove(correct_answers.index(msg))
                
                if indexes:
                    indexchoice = random.choice(indexes)
                    broadcast_msg("i"+str(clients_addr.index(addr))+str(indexchoice),-1)
                else:
                    broadcast_msg("i"+str(clients_addr.index(addr))+str(9),-1)
                
            else:
                conn.send("w".encode(FORMAT))
                    
        else:
            if msg == "r":
                print("preparado")
                print(clients_ready)
                clients_ready[clients_addr.index(addr)] = 1     
                    
            if sum(clients_ready) == threading.active_count() - 1:
                start_game = True
                broadcast_msg("r",-1)                
                time.sleep(0.5)
                broadcast_msg(str(indexchoice),-1)
                time.sleep(0.5)
                broadcast_msg(pickle.dumps(clients_addr),-2)
                print("comenzo el juego")
            else:
                print("Faltan jugadores preparados")            
    print("Conexion cerrada")
    conn.close()

#Función que deja al servidor en escucha y genera un hilo por cada conexión
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

#Código main del servidor que se ejecuta al iniciar
if __name__ == '__main__':
    #Genera el servidor socket
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)

    clients_list = []
    clients_addr = []
    clients_ready = []

    correct_answers = []
    listImgsPath = []

    #Se inicializa las imagenes y sus posibles respuestas para las mismas
    for i in  os.listdir(path="./images"):
        listImgsPath.append(i)
        correct_answers.append(i[:-4])
        
    listImgsPath.sort()
    correct_answers.sort()
                
    indexes = [*range(0,len(listImgsPath),1)]

    indexchoice = random.choice(indexes)
    print("Servidor iniciado...")
    print("Respuestas correctas:")
    print(correct_answers)
    print("actual correcta:",correct_answers[indexchoice])

    start()
