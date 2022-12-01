# -Juego donde en la parte principal sale x figurita y los
# jugadores deben poner el nombre de esa figurita

from tkinter import * #importar la libreria tkinter para hacer la interfaz
import random
import os
from tkinter import messagebox
import socket

HEADER = 1024
PORT = 5050
SERVER = "192.168.0.3"
ADDR = (SERVER,PORT)
FORMAT = 'utf8'
DISCONNECT_MESSAGE = "DISCONNECT"

def cambiarVentana(): # Funcion abrir la ventana del juego
    
    conn = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    conn.connect(ADDR)
    
    def refreshimg():
        global labelImg
        global figuraCentral
        global indexchoice

        labelimg.destroy()
        print(indexes)
        indexchoice = int(conn.recv(1024).decode(FORMAT))
        print("list:",listImgsPath)
        print("choice:",indexchoice)
        ImagenAzar = imgPath + "/" + listImgsPath[indexchoice]
        
        figuraCentral = PhotoImage(file=ImagenAzar) #Figura de ejemplo
        labelImg = Label(ventanaJuego, image = figuraCentral).grid(row = 2, column = 0, columnspan=2, pady = 20) #Insertado en un Label    
        
        
    def enviarDatos(event): # Funcion destruir mensaje tras pulsar el boton de enviar
        mensaje = str(cuadroTexto.get(1.0, "end-1c"))
        
        conn.send(mensaje.encode(FORMAT))
        response = conn.recv(1024).decode(FORMAT)
        if  response == "correcto":
            print("respuesta Correcta")
            refreshimg()
        elif response == "incorrecto":
            print("respuesta Incorrecta")
        elif response == "no preparado":
            print("Aun no puede responder")
        elif response == "preparado":
            print("Listo para responder")
        elif response == "todos listos":
            print("Inicia el juego")
            refreshimg()
        else:
            print("Ingreso invalido")

    global figuraCentral
    
    ventanaJuego = Toplevel() #crear segunda ventana
    ventanaJuego.state(newstate="normal") #poner como estado la segunda ventana como principal
    raiz.state(newstate="withdraw") #retirar la ventana raiz
    ventanaJuego.title =("Ventana del juego")
    ventanaJuego.geometry("700x640")
    ventanaJuego.iconbitmap("niko.ico")
    ventanaJuego.resizable(True,True)

    puntaje = Label(ventanaJuego, text = "Puntaje: " + str(puntajeNum), fg="gray", font=("Verdana", 35)) #Texto puntaje
    puntaje.grid(row = 0, column = 0, columnspan=2, pady = 20) #Insertarlo en un grid

    puntajeAdversario = Label(ventanaJuego, text="Puntaje del adversario1 : X", fg="gray", font=("Verdana", 15)) #Texto puntaje adversario 1
    puntajeAdversario.grid(row = 1, column = 0, padx= 30, pady = 10)
    puntajeAdversario2 = Label(ventanaJuego, text="Puntaje del adversario2 : X", fg="gray", font=("Verdana", 15)) #Texto puntaje adversario 2
    puntajeAdversario2.grid(row = 1, column = 1, padx= 30, pady = 10)


    ImagenAzar = "default.png"
    
    
    figuraCentral = PhotoImage(file=ImagenAzar) #Figura de ejemplo
    labelImg = Label(ventanaJuego, image = figuraCentral).grid(row = 2, column = 0, columnspan=2, pady = 20) #Insertado en un Label    

    cuadroTexto = Text(ventanaJuego, width=50, height=1) #Cuadro de texto
    cuadroTexto.grid(row = 3, column = 0, columnspan=2, pady = 20)

    botonEnviar = Button(ventanaJuego, text="Enviar", fg="gray",font=("Verdana", 15)) #Boton de enviar
    botonEnviar.grid(row = 3, column = 1, columnspan=3)

    puntajeFaltante = Label(ventanaJuego, text="Faltan X puntos para ganar", fg="gray", font=("Verdana", 15)) #Texto de puntaje faltante
    puntajeFaltante.grid(row = 4, column = 0, columnspan=2, padx= 30, pady = 10 )
    
    #cuadroTexto.bind("<Return>",enviarDatos)
    botonEnviar.bind("<Button-1>",enviarDatos)

if __name__ == '__main__':
    raiz = Tk() # Habilitar Interfaz grafica
    raiz.title("Menu principal") # Titulo
    raiz.resizable(True,True) #Activar/Desactivar aumento/reduccion de ventana
    raiz.iconbitmap("niko.ico") # Icono
    # raiz.geometry("700x640") # Resolucion de la ventana
    # raiz.config(bg="#FDFD96") # Color de la ventana

    imgPath = "./images"

    listImgsPath = []
    correct_answers = []

    for i in  os.listdir(path="./images"):
        listImgsPath.append(i)
        correct_answers.append(i[:-4])
    indexes = [*range(0,len(listImgsPath),1)]

    puntajeNum = 10
    labelimg = Label()

    Entrada = Button(raiz, text="Entrar", padx = 50, pady = 50, command=cambiarVentana)
    Entrada.pack(side="top")


    mainloop() # Mantener en loop activo a la Interfaz


# Fuente:
# Interfaces graficas I - Raiz - Python: https://www.youtube.com/watch?v=hTUJC8HsC2I
# Interfaces graficas III - Label y Imagenes - Python: https://www.youtube.com/watch?v=Nf4-gvf-tNg
# Interfaces graficas IV - Cuadro de texto y Grid - Python: https://www.youtube.com/watch?v=YRs8j0QGEn0
# Cuadro de texto con tkinter: https://www.youtube.com/watch?v=2WILKqs9qv0
# Parte de la funcion de destruir mensaje: https://stackoverflow.com/questions/47357090/tkinter-error-couldnt-recognize-data-in-image-file
# Ventanas: https://www.youtube.com/watch?v=D36WS2ER0uk
# Arreglar Imagenes despues de cambiar ventana Tkinter: https://es.stackoverflow.com/questions/493721/python-no-me-carga-una-imagen-solo-aparece-un-cuadro-blanco y
# https://es.stackoverflow.com/questions/335428/abrir-ventana-una-desde-otra-ventana-y-cerrar-la-primera
# to string: https://www.digitalocean.com/community/tutorials/how-to-convert-data-types-in-python-3
# sol variable local: https://es.stackoverflow.com/questions/171863/local-variable-referenced-before-assignment
