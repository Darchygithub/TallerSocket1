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
    global ansText
    global notifLbl
    global sendBtn
    
    jugadorespjes[ind] = jugadorespjes[ind] + 1
    jugadoreslbl[ind].destroy()
    jugadoreslbl[ind] = Label(points_wind,text="Puntos del jugador "+str(jugadores[ind])+ ":  "+ str(jugadorespjes[ind]),font=("Verdana", 15))
    jugadoreslbl[ind].grid(row=ind)
    
    
    if choice != 9:
        indexchoice = choice        
        randomImg = listImgsFile[int(indexchoice)]
        centerImg = ImageTk.PhotoImage(Image.open(imgPath + "/" + randomImg))
    else:
        centerImg = ImageTk.PhotoImage(Image.open("default.png"))
        sendBtn['state'] = DISABLED
        notifLbl['text'] = "Terminado!"
         
        
    imgLbl.destroy()
    imgLbl = Label(game_wind, image = centerImg) #Insertado en un Label
    imgLbl.image = centerImg
    
    imgLbl.grid(row = 2, column = 0, columnspan=2, pady = 20)

    ansText.delete("1.0",END)
    
    
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
    
def get_point(conn):
    global notifLbl
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
            notifLbl["text"] = "Incorrecto"
            time.sleep(0.5)
            notifLbl["text"] = ""
            print("Incorrecto")
        
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
    
    for i in range(len(jugadores)):
        jugadorespjes.append(0)
        jugadoreslbl.append(Label(points_wind,text="Puntos del jugador "+str(jugadores[i])+ ":  "+ str(jugadorespjes[i]),font=("Verdana", 15)))
        jugadoreslbl[i].grid(row=i)
        
    
    
    point_t = threading.Thread(target=get_point, args=(conn,)).start()

    
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
    
    randomImg = listImgsFile[int(indexchoice)]
    centerImg = ImageTk.PhotoImage(Image.open(imgPath + "/" + randomImg)) #Figura de ejemplo    
    
    imgLbl = Label(game_wind, image = centerImg) #Insertado en un Label
    imgLbl.image = centerImg
    
    imgLbl.grid(row = 2, column = 0, columnspan=2, pady = 20)
    
    ansText = Text(game_wind, width=50, height=1) #Cuadro de texto
    ansText.grid(row = 3, column = 0, columnspan=2, pady = 20)

    notifLbl = Label(game_wind,text="",font=("Verdana", 15))
    notifLbl.grid(row = 4, column = 0, columnspan=2, pady = 20)
    
    sendBtn = Button(game_wind, text="Enviar", fg="gray",font=("Verdana", 15),command=lambda: send_ans(conn,ansText.get(1.0,END))) #Boton de enviar
    sendBtn.grid(row = 3, column = 2, columnspan=3)
    
    ansText.bind('<Return>',lambda event: send_ans(conn,ansText.get(1.0,END)))
    
    
    points_screen(conn)
    

if __name__ == '__main__':
    root = Tk() # Habilitar Interfaz grafica
    root.title("Menu principal") # Titulo
    root.resizable(False,False) #Activar/Desactivar aumento/reduccion de ventana
    root.iconbitmap("niko.ico") # Icono
    root.geometry("300x300") # Resolucion de la ventana

    imgPath = "./images"

    listImgsFile = []
    correct_answers = []
    turn = 0
    
    for i in  os.listdir(path="./images"):
        listImgsFile.append(i)
        correct_answers.append(i[:-4])
    
    listImgsFile.sort()
    correct_answers.sort()
    
    indexes = [*range(0,len(listImgsFile),1)]

    enterBtn = Button(root, text="Entrar", padx = 300, pady = 300, command=preparation_screen)
    enterBtn.pack(side="top")


    root.mainloop() # Mantener en loop activo a la Interfaz
