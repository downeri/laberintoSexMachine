import PySimpleGUI as sg
from pyparsing import col

class GUI:
    def elegir(self):
        opcion=0
        sg.theme("DarkGrey5")
        layout=[[sg.Button("Una solución con vida")],[sg.Button("Primer solución encontrada")],[sg.Button("Todas las soluciones")],[sg.Button("Mejor solución")],[sg.Exit()]]
        ventana=sg.Window("Bienvenido",layout,finalize="true")
        while True:
            event,values=ventana.read()
            if event in (None, "Exit"):
                opcion=0
                break
            elif event in (None,"Una solución con vida"):
                opcion=1
                break
            elif event in (None,"Primer solución encontrada"):
                opcion=2
                break
            elif event in (None,"Todas las soluciones"):
                opcion=3
                break
            elif event in (None,"Mejor solución"):
                opcion=4
                break
        ventana.close()
        return opcion
    
    def mensaje(self,titulo,mensaje):
        sg.theme("DarkGrey5")
        layout=[[sg.Text(mensaje)],[sg.Exit()]]
        ventana=sg.Window(titulo,layout,finalize="true")
        while True:
            event,values=ventana.read()
            if event in (None, "Exit"):
                break
        ventana.close()

    def crearGUI(self,columnas,filas,titulo,boton):
        self.filas=filas
        self.columnas=columnas
        self.tamanoDeCeldaX=500/self.columnas
        self.tamanoDeCeldaY=500/self.filas
        sg.theme("DarkGrey5")
        self.layout=[[sg.Canvas(size=(500,500),background_color="white",key="cuad")],[sg.Button(boton)]]
        self.ventana=sg.Window(titulo,self.layout,finalize="true")
        self.cuadricula=self.ventana["cuad"]
        for i in range(self.columnas):
            self.cuadricula.TKCanvas.create_line(self.tamanoDeCeldaX*i,0,self.tamanoDeCeldaX*i,500)
        for i in range(self.filas):
            self.cuadricula.TKCanvas.create_line(0,self.tamanoDeCeldaY*i,500,self.tamanoDeCeldaY*i)  

    def mostrarGUI(self):
        while True:
            event,values=self.ventana.read()
            if event in (None, "Salir") or event in (None, "Siguiente solución"):
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

    def dibujarLaberinto(self,laberinto,coordenadasParedes,coordenadasRaton,coordenadasQueso,r,titulo,boton):
        self.crearGUI(len(laberinto[0]),len(laberinto),titulo,boton)
        for pared in coordenadasParedes:
            self.insertarObjeto(pared)
        self.insertarObjeto(coordenadasRaton,type="raton")
        self.insertarObjeto(coordenadasQueso, type="queso")
        for camino in r[1:len(r)-1]:
            self.insertarObjeto(camino, type="camino")
        self.mostrarGUI()