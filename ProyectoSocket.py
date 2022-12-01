# -Juego donde en la parte principal sale x figurita y los
# jugadores deben poner el nombre de esa figurita

from tkinter import * #importar la libreria tkinter para hacer la interfaz
import random
from tkinter import messagebox

raiz = Tk() # Habilitar Interfaz grafica
raiz.title("Menu principal") # Titulo
raiz.resizable(True,True) #Activar/Desactivar aumento/reduccion de ventana
raiz.iconbitmap("niko.ico") # Icono
# raiz.geometry("700x640") # Resolucion de la ventana
# raiz.config(bg="#FDFD96") # Color de la ventana

global puntajeNum
puntajeNum = 10
def cambiarVentana(): # Funcion abrir la ventana del juego

    def enviarDatos(): # Funcion destruir mensaje tras pulsar el boton de enviar
        
        global puntajeNum
        mensaje = str(cuadroTexto.get(1.0, "end-1c"))
        print(respuestaCorrecta)
        if mensaje == respuestaCorrecta:
            print("respuesta Correcta")
            messagebox.showinfo(message="Respuesta Correcta", title="LOL")
            print(mensaje)
            cuadroTexto.delete(1.0, END)
            puntajeNum = puntajeNum - 1
            ventanaJuego.after(1000, cambiarVentana)
        else:
            print("respuesta Incorrecta")
            print(mensaje)
            cuadroTexto.delete(1.0, END)

    ventanaJuego = Toplevel() #crear segunda ventana
    ventanaJuego.state(newstate="normal") #poner como estado la segunda ventana como principal
    raiz.state(newstate="withdraw") #retirar la ventana raiz
    ventanaJuego.title =("Ventana del juego")
    ventanaJuego.geometry("700x640")
    ventanaJuego.iconbitmap("niko.ico")
    ventanaJuego.resizable(True,True)


    print(str(puntajeNum))
    puntaje = Label(ventanaJuego, text = "Puntaje: ", textvariable=str(puntajeNum), fg="gray", font=("Verdana", 35)) #Texto puntaje

    puntaje.grid(row = 0, column = 0, columnspan=2, pady = 20) #Insertarlo en un grid

    puntajeAdversario = Label(ventanaJuego, text="Puntaje del adversario1 : X", fg="gray", font=("Verdana", 15)) #Texto puntaje adversario 1
    puntajeAdversario.grid(row = 1, column = 0, padx= 30, pady = 10)
    puntajeAdversario2 = Label(ventanaJuego, text="Puntaje del adversario2 : X", fg="gray", font=("Verdana", 15)) #Texto puntaje adversario 2
    puntajeAdversario2.grid(row = 1, column = 1, padx= 30, pady = 10)

    listaImagenes = ['manzana.png','tomate.png','platano.png','sushi.png','hamburguesa.png']

    ImagenAzar = random.choice(listaImagenes)
    global figuraCentral
    global respuestaCorrecta

    if  ImagenAzar == 'manzana.png':
        respuestaCorrecta = 'manzana'
    elif ImagenAzar == "tomate.png":
        respuestaCorrecta = 'tomate'
    elif ImagenAzar == "platano.png":
        respuestaCorrecta = 'platano'
    elif ImagenAzar == "sushi.png":
        respuestaCorrecta = 'sushi'
    elif ImagenAzar == "hamburguesa.png":
        respuestaCorrecta = 'hamburguesa'
    print(respuestaCorrecta)
    figuraCentral = PhotoImage(file=ImagenAzar) #Figura de ejemplo
    Label(ventanaJuego, image = figuraCentral).grid(row = 2, column = 0, columnspan=2, pady = 20) #Insertado en un Label

    cuadroTexto = Text(ventanaJuego, width=50, height=1) #Cuadro de texto
    cuadroTexto.grid(row = 3, column = 0, columnspan=2, pady = 20)

    botonEnviar = Button(ventanaJuego, text="Enviar", fg="gray",font=("Verdana", 15), command=enviarDatos) #Boton de enviar
    botonEnviar.grid(row = 3, column = 1, columnspan=3)

    puntajeFaltante = Label(ventanaJuego, text="Faltan X puntos para ganar", fg="gray", font=("Verdana", 15)) #Texto de puntaje faltante
    puntajeFaltante .grid(row = 4, column = 0, columnspan=2, padx= 30, pady = 10 )

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
