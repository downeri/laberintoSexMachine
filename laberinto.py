from copy import deepcopy
import json
from pydoc import importfile
import PySimpleGUI as sg
from gui import GUI
from funcionesUnicaSolucion import unica as us
from funcionesSolucionVida import fvida as sv
from funcionesTodasLasSoluciones import todas as ts

def obtener_configuracion(laberinto,coordenadasQueso,coordenadasRaton,coordenadasParedes):
    gui=GUI()
    with open("config.json") as f:
        configuracion=json.load(f)
    columnas=len(configuracion["laberinto"][0][0])
    for i in range(len(configuracion["laberinto"])):
        if columnas!=len(configuracion["laberinto"][i][0]):
            print(f"Las columnas de la fila {i} no coinciden con las columnas establecidas en la fila 0")
            return None,None
        laberinto.append(configuracion["laberinto"][i][0].split())
        for u in range(len(laberinto[i])):
            if laberinto[i][u]=="R":
                coordenadasRaton.append(u)
                coordenadasRaton.append(i)
            elif laberinto[i][u]=="Q":
                coordenadasQueso.append(u)
                coordenadasQueso.append(i)
            elif laberinto[i][u]=="X":
                coordenadasParedes.append([u,i])
    if coordenadasQueso==[]:
        gui.mensaje("Error","No se encontró el queso")
        return None,None
    if coordenadasRaton==[]:
        gui.mensaje("Error","No se encontró el ratón")
        return None,None
    if configuracion["tieneVida"]==True:
        vida=configuracion["vida"].copy()
        return True,vida
    return True,None

def main(): 
    laberinto=[]
    coordenadasRaton=[]
    coordenadasQueso=[]
    coordenadasParedes=[]
    estado=[]
    gui=GUI()
    x,vida=obtener_configuracion(laberinto,coordenadasQueso,coordenadasRaton,coordenadasParedes)
    estado.append(coordenadasRaton)
    if x!=None:
        seleccion=gui.elegir()
        if seleccion==1:
            if vida==None:
                gui.mensaje("Vida infinita","El laberinto no tiene la vida habilitada, mostrando solución unica con vida ilimitada")
                seleccion=2
            else:
                opciones=sv.obtenerOpcionesVida(coordenadasRaton,coordenadasParedes,estado,[len(laberinto[0]),len(laberinto)],vida)
                r=sv.encontrarConVida(sv,coordenadasQueso,opciones,estado,coordenadasParedes,[len(laberinto[0]),len(laberinto)],vida)
                if r==False:
                    gui.mensaje("Sin solución","No se encontró un camino para el queso")
                else:
                    v=vida["vidaTotal"]
                    gui.dibujarLaberinto(laberinto,coordenadasParedes,coordenadasRaton,coordenadasQueso,r[0],f"Laberinto | Con vida | Vida usada: {v-r[1]}/{v} puntos","Salir")
        if seleccion==2:
            opciones=us.obtenerOpciones(coordenadasRaton,coordenadasParedes,estado,[len(laberinto[0]),len(laberinto)])
            r=us.encontrar(us,coordenadasQueso,opciones,estado,coordenadasParedes,[len(laberinto[0]),len(laberinto)])
            if r==False:
                gui.mensaje("Sin solución","No se encontró un camino para el queso")
            else:
                gui.dibujarLaberinto(laberinto,coordenadasParedes,coordenadasRaton,coordenadasQueso,r,"Laberinto | Unica solución","Salir")
        if seleccion==3:
            respuestas=[]
            opciones=us.obtenerOpciones(coordenadasRaton,coordenadasParedes,estado,[len(laberinto[0]),len(laberinto)])
            ts.encontrarTodasPosibilidades(ts,coordenadasQueso,opciones,estado,coordenadasParedes,[len(laberinto[0]),len(laberinto)],respuestas)
            if len(respuestas)!=0:
                i=0
                for respuesta in respuestas:
                    i+=1
                    if(i!=len(respuestas)):
                        gui.dibujarLaberinto(laberinto,coordenadasParedes,coordenadasRaton,coordenadasQueso,respuesta,f"Laberinto | Solución {i}/{len(respuestas)}","Siguiente solución")
                    else:
                        gui.dibujarLaberinto(laberinto,coordenadasParedes,coordenadasRaton,coordenadasQueso,respuesta,f"Laberinto | Solución {i}/{len(respuestas)}","Salir")
            else:
                gui.mensaje("Sin solución","No se encontró un camino para el queso")  
            
if __name__=="__main__":
    main()
