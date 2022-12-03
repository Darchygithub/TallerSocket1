import socket
import threading
import os
import random
import pickle
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

def player_point(name,msg,newindex):
    for client in clients_addr:
        client.send(name+" "+msg+" "+str(newindex))
    

def handle_client(conn,addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    start_game = False
    connected = True
    while connected:
        global start_flags
        
        try:
            msg = conn.recv(HEADER).decode(FORMAT).strip()
            #if start_game:
                
            if start_flags == threading.active_count() - 1 :
                start_game = True
                print("TODOS PREPARADOS")
                conn.send("todos listos".encode(FORMAT))
                conn.recv(HEADER).decode(FORMAT)
                for client in clients_list:
                    data = pickle.dumps(clients_addr)
                    client.send(data)
                print("Flag 1 serv")
                conn.recv(HEADER).decode(FORMAT)
                print("Flag 2 serv con indice ",indexchoice)
                for client in clients_list:
                    client.send(str(indexchoice).encode(FORMAT))
                '''
                if msg in correct_answers:                
                    listImgsPath.pop(indexchoice)
                    indexes.pop(indexchoice)
                    correct_answers.pop(indexchoice)
                    
                    indexchoice = random.choice(indexes)
                    print(f"Player direccion ",addr," obtuvo punto")
                    print("Nuevas respuestas correctas:")
                    print(correct_answers)
                    print("actual correcta:",correct_answers[indexchoice])

                    player_point(addr," correcto ",indexchoice)
                else:
                    print(f"Player direccion ",addr," incorrecto")
                    conn.send("incorrecto".encode(FORMAT))
                    '''
                
            elif msg == "r":
                start_flags = start_flags + 1
                conn.send("preparado".encode(FORMAT))
            else:
                conn.send("no preparado".encode(FORMAT))
            print(f"[{addr}] {msg}")
        except:
            if conn in clients_list:
                clients_list.remove(conn)
                clients_addr.remove(addr)
                print(addr," Removido")        
        
    conn.close()
    
def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        
        clients_list.append(conn)
        clients_addr.append(addr)
        print(len(clients_list))
        thread = threading.Thread(target=handle_client, args=(conn,addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1 }")

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

clients_list = []
clients_addr = []
start_flags = 0

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

'''
if mensaje == correct_answers[indexchoice]:
    
    messagebox.showinfo(message="Respuesta Correcta", title="LOL")
    
    cuadroTexto.delete(1.0, END)
    
    global puntajeNum 
    
    
    puntajeNum = puntajeNum - 1
    
    for i in range(indexes[indexchoice],len(indexes)):
        print(i)
        indexes[i] -= 1

    listImgsPath.pop(indexchoice)
    indexes.pop(indexchoice)
    correct_answers.pop(indexchoice)
        
    refreshimg()
    cuadroTexto.delete(1.0, END)
else:
    print("respuesta Incorrecta")
    print(mensaje)
    cuadroTexto.delete(1.0, END)
'''

#https://www.youtube.com/watch?v=3QiPPX-KeSc
#https://www.youtube.com/watch?v=lGL1XZfix-w