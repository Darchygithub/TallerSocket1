from tkinter import * 
import os
from tkinter import StringVar #,messagebox
import socket
import pickle
from PIL import Image,ImageTk
import threading
import time

HEADER = 1024
PORT = 5050
SERVER = "192.168.0.7"
ADDR = (SERVER,PORT)
FORMAT = 'utf8'
DISCONNECT_MESSAGE = "DISCONNECT"

def send_ans(conn,msg):
    conn.send(msg.encode(FORMAT))
    result = conn.recv(HEADER).decode(FORMAT).strip()
    print(result)
    if result[0] == "i":
        print("correcto")
        ind = int(result[1])
        indexchoice = int(result[2])
        jugadorespjes[ind] = jugadorespjes[ind] + 1
        jugadoreslbl[ind].destroy()
        jugadoreslbl[ind] = Label(points_wind,text="Puntos del jugador "+str(jugadores[ind])+ ":  "+ str(jugadorespjes[ind]),font=("Verdana", 15))
        jugadoreslbl[ind].grid(row=ind)      
        
        randomImg = listImgsFile[int(indexchoice)]
        centerImg = ImageTk.PhotoImage(Image.open(imgPath + "/" + randomImg)) #Figura de ejemplo    
        
        global imgLbl
        
        imgLbl.destroy()
        imgLbl = Label(game_wind, image = centerImg) #Insertado en un Label
        imgLbl.image = centerImg
        
        imgLbl.grid(row = 2, column = 0, columnspan=2, pady = 20)          
    elif result == "w":
        print("incorrecto")
    
    
def ready_msg(conn,wind):
    #messagebox.showinfo(message="Espere a los demas jugadores")
    conn.settimeout(100)
    conn.send("r".encode(FORMAT))
    start = conn.recv(HEADER).decode(FORMAT)
    if start == "r":
        print("comenzo el juego")
        wind.destroy()
        game_screen(conn)

def give_player_point(ind,choice):
    print("punto jugador")
    print(jugadorespjes)
    print(ind)
    
    global imgLbl
    
    jugadorespjes[ind] = jugadorespjes[ind] + 1
    jugadoreslbl[ind].destroy()
    jugadoreslbl[ind] = Label(points_wind,text="Puntos del jugador "+str(jugadores[ind])+ ":  "+ str(jugadorespjes[ind]),font=("Verdana", 15))
    jugadoreslbl[ind].grid(row=ind)
    
    indexchoice = choice
    
    randomImg = listImgsFile[int(indexchoice)]
    centerImg = ImageTk.PhotoImage(Image.open(imgPath + "/" + randomImg)) #Figura de ejemplo    
    
    imgLbl.destroy()
    imgLbl = Label(game_wind, image = centerImg) #Insertado en un Label
    imgLbl.image = centerImg
    
    imgLbl.grid(row = 2, column = 0, columnspan=2, pady = 20)
        
def preparation_screen():
    
    conn = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    conn.connect(ADDR)
    
    prep_wind = Toplevel()
    prep_wind.title("Players")
    prep_wind.geometry("300x600+900+100")
    prep_wind.resizable(False,False)
    
    readyBtn = Button(prep_wind, text="Enviar", fg="gray",font=("Verdana", 15),command=lambda: ready_msg(conn,prep_wind)) #Boton de enviar
    readyBtn.grid(row = 0, column = 0, columnspan=3)
    

    root.withdraw()
    
    #game_screen()

def get_point(conn):
    while True:
        time.sleep(0.5)
        point_player = None
        point_player = conn.recv(HEADER).decode(FORMAT,errors='replace').strip()
        if point_player[0] == "i":           
            print(point_player)
            give_player_point(int(point_player[1]),int(point_player[2]))
        
def points_screen(conn):
    global jugadores
    jugadores = pickle.loads(conn.recv(HEADER))
    
    global jugadorespjes
    global jugadoreslbl
    jugadorespjes = []
    jugadoreslbl = []
    global points_wind
    points_wind = Toplevel()
    points_wind.title("Players")
    points_wind.geometry("600x600+900+100")
    points_wind.resizable(False,False)
    
    for i in range(len(jugadores)):
        jugadorespjes.append(0)
        jugadoreslbl.append(Label(points_wind,text="Puntos del jugador "+str(jugadores[i])+ ":  "+ str(jugadorespjes[i]),font=("Verdana", 15)))
        jugadoreslbl[i].grid(row=i)
        
    
    
    point_t = threading.Thread(target=get_point, args=(conn,)).start()

    
def game_screen(conn):
    global game_wind
    game_wind = Toplevel()
    game_wind.title("Game")
    game_wind.geometry("600x600+300+100")
    game_wind.resizable(False,False)
    
    global indexchoice
    
    indexchoice = conn.recv(HEADER).decode(FORMAT)
    
    global imgLbl
    
    randomImg = listImgsFile[int(indexchoice)]
    centerImg = ImageTk.PhotoImage(Image.open(imgPath + "/" + randomImg)) #Figura de ejemplo    
    
    imgLbl = Label(game_wind, image = centerImg) #Insertado en un Label
    imgLbl.image = centerImg
    
    imgLbl.grid(row = 2, column = 0, columnspan=2, pady = 20)
    
    cuadroTexto = Text(game_wind, width=50, height=1) #Cuadro de texto
    cuadroTexto.grid(row = 3, column = 0, columnspan=2, pady = 20)

    botonEnviar = Button(game_wind, text="Enviar", fg="gray",font=("Verdana", 15),command=lambda: send_ans(conn,cuadroTexto.get(1.0,END))) #Boton de enviar
    botonEnviar.grid(row = 3, column = 2, columnspan=3)
    
    points_screen(conn)
    

if __name__ == '__main__':
    root = Tk() # Habilitar Interfaz grafica
    root.title("Menu principal") # Titulo
    root.resizable(False,False) #Activar/Desactivar aumento/reduccion de ventana
    root.iconbitmap("niko.ico") # Icono
    root.geometry("600x300") # Resolucion de la ventana

    imgPath = "./images"

    listImgsFile = []
    correct_answers = []
    turn = 0
    
    for i in  os.listdir(path="./images"):
        listImgsFile.append(i)
        correct_answers.append(i[:-4])
    indexes = [*range(0,len(listImgsFile),1)]

    enterBtn = Button(root, text="Entrar", padx = 500, pady = 500, command=preparation_screen)
    enterBtn.pack(side="top")


    root.mainloop() # Mantener en loop activo a la Interfaz
