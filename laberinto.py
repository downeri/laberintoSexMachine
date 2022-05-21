from copy import deepcopy
import json
from pydoc import importfile
from re import X
import PySimpleGUI as sg
import numpy as np
from gui import GUI

def obtener_configuracion(laberinto,coordenadasQueso,coordenadasRaton,coordenadasParedes):
    with open("config.json") as f:
        configuracion=json.load(f)

    columnas=len(configuracion["laberinto"][0][0])
    for i in range(len(configuracion["laberinto"])):
        if columnas!=len(configuracion["laberinto"][i][0]):
            print(f"Las columnas de la fila {i} no coinciden con las columnas establecidas en la fila 0")
            return None
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
        print("No se encontró el queso")
        return None,None
    if coordenadasRaton==[]:
        print("No se encontró el ratón")
        return None,None
    if configuracion["tieneVida"]==True:
        vida=configuracion["vida"].copy()
        return True,vida
    return True,None

def obtenerOpciones(posicion,coordenadasParedes,estado,tamanoLab):
    xPositivo=[posicion[0]+1,posicion[1]]
    xNegativo=[posicion[0]-1,posicion[1]]
    yPositivo=[posicion[0],posicion[1]+1]
    yNegativo=[posicion[0],posicion[1]-1]
    opciones=[xPositivo,xNegativo,yPositivo,yNegativo]
    if xPositivo in coordenadasParedes or xPositivo[0]>tamanoLab[0]-1 or xPositivo in estado :
        opciones.remove(xPositivo)
    if xNegativo in coordenadasParedes or xNegativo[0]<0 or xNegativo in estado:
        opciones.remove(xNegativo)
    if yPositivo in coordenadasParedes or yPositivo[1]<0 or yPositivo in estado:
        opciones.remove(yPositivo)
    if yNegativo in coordenadasParedes or yNegativo[1]>tamanoLab[1]-1 or yNegativo in estado:
        opciones.remove(yNegativo)
    return opciones

def encontrar(objetivo,opciones,estado,coordenadasParedes,tamanoLab):
    if objetivo in opciones:
        estadoTemp=deepcopy(estado)
        estadoTemp.append(objetivo)
        return estadoTemp
    elif len(opciones)==0:
        return False
    for opcion in opciones:
        estadoTemp=deepcopy(estado)
        estadoTemp.append(opcion)
        nuevasOpciones=obtenerOpciones(opcion,coordenadasParedes,estadoTemp,tamanoLab)
        print(nuevasOpciones)
        r=encontrar(objetivo,nuevasOpciones,estadoTemp,coordenadasParedes,tamanoLab)
        if r!=False:
            return r
    return False

def main():
    laberinto=[]
    coordenadasRaton=[]
    coordenadasQueso=[]
    coordenadasParedes=[]
    estado=[]
    x,vida=obtener_configuracion(laberinto,coordenadasQueso,coordenadasRaton,coordenadasParedes)
    estado.append(coordenadasRaton)
    if x!=None:
        opciones=obtenerOpciones(coordenadasRaton,coordenadasParedes,estado,[len(laberinto[0]),len(laberinto)])
        r=encontrar(coordenadasQueso,opciones,estado,coordenadasParedes,[len(laberinto[0]),len(laberinto)])
        if r==False:
            print("No se encontró el queso")
        else:
            gui=GUI()
            gui.crearGUI(len(laberinto[0]),len(laberinto))
            for pared in coordenadasParedes:
                gui.insertarObjeto(pared)
            gui.insertarObjeto(coordenadasRaton,type="raton")
            gui.insertarObjeto(coordenadasQueso, type="queso")
            for camino in r[1:len(r)-1]:
                gui.insertarObjeto(camino, type="camino")
            gui.mostrarGUI()
        
if __name__=="__main__":
    main()
