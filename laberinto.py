import json
from pydoc import importfile
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
                coordenadasRaton.append([u,i])
            elif laberinto[i][u]=="Q":
                coordenadasQueso.append([u,i])
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

def main():
    laberinto=[]
    coordenadasRaton=[]
    coordenadasQueso=[]
    coordenadasParedes=[]
    x,vida=obtener_configuracion(laberinto,coordenadasQueso,coordenadasRaton,coordenadasParedes)
    if x!=None:
        gui=GUI()
        gui.crearGUI(len(laberinto[0]),len(laberinto))
        for pared in coordenadasParedes:
            gui.insertarObjeto(pared)
        gui.insertarObjeto(coordenadasRaton[0],type="raton")
        gui.insertarObjeto(coordenadasQueso[0], type="queso")
        gui.mostrarGUI()
        
    

if __name__=="__main__":
    main()
