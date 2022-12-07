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

#Función que envia un mensaje y lo codifica en el formato específico
def send_ans(conn,msg):
    conn.send(msg.encode(FORMAT))
    
#Función que indica al servidor si el jugador está listo
def ready_msg(conn,wind):    
    conn.settimeout(100)
    conn.send("r".encode(FORMAT))
    start = conn.recv(HEADER).decode(FORMAT)
    if start == "r":
        print("comenzo el juego")
        wind.destroy()
        game_screen(conn)

#Función que realiza el proceso de dar el puntaje a un jugador
def give_player_point(ind,choice):
    print("punto jugador")
    
    global imgLbl
    global ansText
    global notifLbl
    global sendBtn
    
    #Etiqueta específica del jugador que gana el punto
    jugadorespjes[ind] = jugadorespjes[ind] + 1
    jugadoreslbl[ind].destroy()
    jugadoreslbl[ind] = Label(points_wind,text="Puntos del jugador "+str(jugadores[ind])+ ":  "+ str(jugadorespjes[ind]),font=("Verdana", 15))
    jugadoreslbl[ind].grid(row=ind)
        
    #Condición que indica el último turno
    if choice != 9:
        indexchoice = choice        
        randomImg = listImgsFile[int(indexchoice)]
        centerImg = ImageTk.PhotoImage(Image.open(imgPath + "/" + randomImg))
    else:
        centerImg = ImageTk.PhotoImage(Image.open("default.png"))
        sendBtn['state'] = DISABLED
        notifLbl['text'] = "Terminado!"
         
    #Actualiza la imagen central        
    imgLbl.destroy()
    imgLbl = Label(game_wind, image = centerImg)
    imgLbl.image = centerImg
    
    imgLbl.grid(row = 2, column = 0, columnspan=2, pady = 20)

    ansText.delete("1.0",END)
    
#Funcion de pantalla de preparación para "sincronizar" los clientes
def preparation_screen():    
    conn = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    conn.connect(ADDR)
    
    prep_wind = Toplevel()
    prep_wind.title("Players")
    prep_wind.geometry("300x300")
    prep_wind.resizable(False,False)
    
    readyBtn = Button(prep_wind, text="Conectar", fg="gray",font=("Verdana", 15),command=lambda: ready_msg(conn,prep_wind), padx=100, pady=130) #Boton de enviar
    readyBtn.grid(row = 0, column = 0, columnspan=3)
    

    root.withdraw()
    
#Función que permite al cliente recibir un mensaje del servidor en cualquier momento.
def get_point(conn):
    global notifLbl
    global ansText
    while True:
        point_player = None
        point_player = conn.recv(HEADER).decode(FORMAT,errors='replace').strip()
        if point_player[0] == "i":           
            print(point_player)
            notifLbl["text"] = "Correcto!"
            time.sleep(0.1)
            notifLbl["text"] = ""
            give_player_point(int(point_player[1]),int(point_player[2]))
        elif point_player == "endgame":
            give_player_point(int(point_player[1]),int(point_player[2]))
        elif point_player == "w":
            ansText.delete("1.0",END)
            notifLbl["text"] = "Incorrecto"
            time.sleep(0.5)
            notifLbl["text"] = ""
            print("Incorrecto")

#Función que genera la pantalla donde se muestran los puntajes de los jugadores
def points_screen(conn):
    global jugadores
    global jugadorespjes
    global jugadoreslbl
    global points_wind
    jugadores = pickle.loads(conn.recv(HEADER))
    
    jugadorespjes = []
    jugadoreslbl = []
    points_wind = Toplevel()
    points_wind.title("Players")
    points_wind.geometry("600x600+900+100")
    points_wind.resizable(False,False)
    
    #Crea la etiqueta por cada jugador
    for i in range(len(jugadores)):
        jugadorespjes.append(0)
        jugadoreslbl.append(Label(points_wind,text="Puntos del jugador "+str(jugadores[i])+ ":  "+ str(jugadorespjes[i]),font=("Verdana", 15)))
        jugadoreslbl[i].grid(row=i)
        
    point_t = threading.Thread(target=get_point, args=(conn,)).start()

#Función que genera la pantalla de juego principal
def game_screen(conn):
    global game_wind
    global indexchoice
    global imgLbl
    global ansText
    global notifLbl
    global sendBtn
    
    game_wind = Toplevel()
    game_wind.title("Game")
    game_wind.geometry("600x600+300+100")
    game_wind.resizable(False,False)

    indexchoice = conn.recv(HEADER).decode(FORMAT)
    print(indexchoice)
    print(listImgsFile)
    
    #Se genera los componentes principales de la interfaz de usuario
    randomImg = listImgsFile[int(indexchoice)]
    centerImg = ImageTk.PhotoImage(Image.open(imgPath + "/" + randomImg)) 
    
    imgLbl = Label(game_wind, image = centerImg) 
    imgLbl.image = centerImg
    
    imgLbl.grid(row = 2, column = 0, columnspan=2, pady = 20)
    
    ansText = Text(game_wind, width=50, height=1) 
    ansText.grid(row = 3, column = 0, columnspan=2, pady = 20)

    notifLbl = Label(game_wind,text="",font=("Verdana", 15))
    notifLbl.grid(row = 4, column = 0, columnspan=2, pady = 20)
    
    sendBtn = Button(game_wind, text="Enviar", fg="gray",font=("Verdana", 15),command=lambda: send_ans(conn,ansText.get(1.0,END))) 
    sendBtn.grid(row = 3, column = 2, columnspan=3)
    
    ansText.bind('<Return>',lambda event: send_ans(conn,ansText.get(1.0,END)))
    
    points_screen(conn)
    
#Código main de la aplicación que se ejecuta al iniciar
if __name__ == '__main__':
    #Genera una ventana con su configuración
    root = Tk() 
    root.title("Menu principal") 
    root.resizable(False,False) 
    root.iconbitmap("niko.ico") 
    root.geometry("300x300")

    #Se inicializan las imagenes para el juego
    imgPath = "./images"

    listImgsFile = []
 
    for i in  os.listdir(path="./images"):
        listImgsFile.append(i)
    
    listImgsFile.sort()
    
    enterBtn = Button(root, text="Entrar", padx = 300, pady = 300, command=preparation_screen)
    enterBtn.pack(side="top")

    #Mantiene la aplicación siempre funcionando en un loop
    root.mainloop() 
