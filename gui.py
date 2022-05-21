import PySimpleGUI as sg
from pyparsing import col

class GUI:
    def mensaje(self,titulo,mensaje):
        sg.theme("DarkGrey5")
        layout=[[sg.Text(mensaje)],[sg.Exit()]]
        ventana=sg.Window(titulo,layout,finalize="true")
        while True:
            event,values=ventana.read()
            if event in (None, "Exit"):
                break
        ventana.close()

    def crearGUI(self,columnas,filas):
        self.filas=filas
        self.columnas=columnas
        self.tamanoDeCeldaX=500/self.columnas
        self.tamanoDeCeldaY=500/self.filas
        sg.theme("DarkGrey5")
        self.layout=[[sg.Canvas(size=(500,500),background_color="white",key="cuad")],[sg.Exit()]]
        self.ventana=sg.Window("Laberinto",self.layout,finalize="true")
        self.cuadricula=self.ventana["cuad"]
        for i in range(self.columnas):
            self.cuadricula.TKCanvas.create_line(self.tamanoDeCeldaX*i,0,self.tamanoDeCeldaX*i,500)
        for i in range(self.filas):
            self.cuadricula.TKCanvas.create_line(0,self.tamanoDeCeldaY*i,500,self.tamanoDeCeldaY*i)  

    def mostrarGUI(self):
        while True:
            event,values=self.ventana.read()
            if event in (None, "Exit"):
                break
        self.ventana.close()

    def insertarObjeto(self,coords,type="pared"):
        if type=="pared":
            self.cuadricula.TKCanvas.create_rectangle(coords[0]*self.tamanoDeCeldaX,coords[1]*self.tamanoDeCeldaY,coords[0]*self.tamanoDeCeldaX+self.tamanoDeCeldaX,coords[1]*self.tamanoDeCeldaY+self.tamanoDeCeldaY, fill="GREY")
        elif type=="raton":
            self.cuadricula.TKCanvas.create_rectangle(coords[0]*self.tamanoDeCeldaX,coords[1]*self.tamanoDeCeldaY,coords[0]*self.tamanoDeCeldaX+self.tamanoDeCeldaX,coords[1]*self.tamanoDeCeldaY+self.tamanoDeCeldaY, fill="PINK")
        elif type=="queso":
            self.cuadricula.TKCanvas.create_rectangle(coords[0]*self.tamanoDeCeldaX,coords[1]*self.tamanoDeCeldaY,coords[0]*self.tamanoDeCeldaX+self.tamanoDeCeldaX,coords[1]*self.tamanoDeCeldaY+self.tamanoDeCeldaY, fill="YELLOW")
        elif type=="camino":
            self.cuadricula.TKCanvas.create_rectangle(coords[0]*self.tamanoDeCeldaX,coords[1]*self.tamanoDeCeldaY,coords[0]*self.tamanoDeCeldaX+self.tamanoDeCeldaX,coords[1]*self.tamanoDeCeldaY+self.tamanoDeCeldaY, fill="#91eb7a")