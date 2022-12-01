import socket
import threading
#AGREGAR CAMBIO MENSAJE MINUSCULAS

HEADER = 1024
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER,PORT)
FORMAT = 'utf8'
DISCONNECT_MESSAGE = "DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def sumar_punto(conn):
    print("Realizando suma de punto")
    conn.send("sumar punto".encode(FORMAT))
    
def actividad2():
    print("Realizando actividad2")

def handle_client(conn,addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    
    connected = True
    while connected:
        msg = conn.recv(HEADER).decode(FORMAT)
        if msg == DISCONNECT_MESSAGE:
            connected = False
        elif msg == "sumar punto":
            sumar_punto(conn)
        print(f"[{addr}] {msg}")
    conn.close()
    
def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn,addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1 }")

        
print("Servidor iniciado...")
start()