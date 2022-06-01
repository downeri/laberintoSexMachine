from copy import deepcopy
import json
from pydoc import importfile
import PySimpleGUI as sg
from gui import GUI

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
    if yPositivo in coordenadasParedes or yPositivo[1]>tamanoLab[1]-1 or yPositivo in estado:
        opciones.remove(yPositivo)
    if yNegativo in coordenadasParedes or yNegativo[1]<0 or yNegativo in estado:
        opciones.remove(yNegativo)
    return opciones

def obtenerOpcionesVida(posicion,coordenadasParedes,estado,tamanoLab,vida):
    xPositivo=[posicion[0]+1,posicion[1]]
    xNegativo=[posicion[0]-1,posicion[1]]
    yPositivo=[posicion[0],posicion[1]+1]
    yNegativo=[posicion[0],posicion[1]-1]
    opciones=[[xPositivo,xNegativo,yPositivo,yNegativo]]
    movimiento=["H","H","V","V"]
    if xPositivo in coordenadasParedes or xPositivo[0]>tamanoLab[0]-1 or xPositivo in estado or vida["vidaTotal"]-vida["vidaHorizontal"]<0:
        movimiento.pop(opciones[0].index(xPositivo))
        opciones[0].remove(xPositivo) 
    if xNegativo in coordenadasParedes or xNegativo[0]<0 or xNegativo in estado or vida["vidaTotal"]-vida["vidaHorizontal"]<0:
        movimiento.pop(opciones[0].index(xNegativo))
        opciones[0].remove(xNegativo)
    if yPositivo in coordenadasParedes or yPositivo[1]>tamanoLab[1]-1 or yPositivo in estado or vida["vidaTotal"]-vida["vidaVertical"]<0:
        movimiento.pop(opciones[0].index(yPositivo))
        opciones[0].remove(yPositivo)
    if yNegativo in coordenadasParedes or yNegativo[1]<0 or yNegativo in estado  or vida["vidaTotal"]-vida["vidaVertical"]<0:
        movimiento.pop(opciones[0].index(yNegativo))
        opciones[0].remove(yNegativo)
    opciones.append(movimiento)
    return opciones

def encontrarConVida(objetivo,opciones,estado,coordenadasParedes,tamanoLab,vida):
    i=0
    if objetivo in opciones[0]:
        u=opciones[0].index(objetivo)
        vidaTemp=deepcopy(vida)
        if opciones[0][u][0]-objetivo[0]==1:
            vidaTemp["vidaTotal"]-=vidaTemp["vidaHorizontal"]
        else:
            vidaTemp["vidaTotal"]-=vidaTemp["vidaVertical"]
        if vidaTemp["vidaTotal"]>=0:
            estadoTemp=deepcopy(estado)
            estadoTemp.append(objetivo)
            r=[estadoTemp,vidaTemp["vidaTotal"]]
            return r
        return False
    elif len(opciones[0])==0:
        return False
    for opcion in opciones[0]:
        vidaTemp=deepcopy(vida)
        if opciones[1][i]=="H":
            vidaTemp["vidaTotal"]-=vidaTemp["vidaHorizontal"]
        else:
            vidaTemp["vidaTotal"]-=vidaTemp["vidaVertical"]
        estadoTemp=deepcopy(estado)
        estadoTemp.append(opcion)
        nuevasOpciones=obtenerOpcionesVida(opcion,coordenadasParedes,estadoTemp,tamanoLab,vidaTemp)
        r=encontrarConVida(objetivo,nuevasOpciones,estadoTemp,coordenadasParedes,tamanoLab,vidaTemp)
        if r!=False:
            return r
        i+=1
    return False

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
        r=encontrar(objetivo,nuevasOpciones,estadoTemp,coordenadasParedes,tamanoLab)
        if r!=False:
            return r
    return False

def encontrarTodasPosibilidades(objetivo,opciones,estado,coordenadasParedes,tamanoLab,respuestas):
    if objetivo in opciones:
        estado.append(objetivo)
        respuestas.append(estado)
    elif len(opciones)==0:
        return False
    for opcion in opciones:
        estadoTemp=deepcopy(estado)
        estadoTemp.append(opcion)
        nuevasOpciones=obtenerOpciones(opcion,coordenadasParedes,estadoTemp,tamanoLab)
        encontrarTodasPosibilidades(objetivo,nuevasOpciones,estadoTemp,coordenadasParedes,tamanoLab,respuestas)
    if len(respuestas)==0:
        return False
    return True

def dibujarLaberinto(gui,laberinto,coordenadasParedes,coordenadasRaton,coordenadasQueso,r,titulo,boton):
    gui.crearGUI(len(laberinto[0]),len(laberinto),titulo,boton)
    for pared in coordenadasParedes:
        gui.insertarObjeto(pared)
    gui.insertarObjeto(coordenadasRaton,type="raton")
    gui.insertarObjeto(coordenadasQueso, type="queso")
    for camino in r[1:len(r)-1]:
        gui.insertarObjeto(camino, type="camino")
    gui.mostrarGUI()

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
        seleccion=gui.elejir()
        if seleccion==1:
            if vida==None:
                gui.mensaje("Vida infinita","El laberinto no tiene la vida habilitada, mostrando solución unica con vida ilimitada")
                seleccion=2
            else:
                opciones=obtenerOpcionesVida(coordenadasRaton,coordenadasParedes,estado,[len(laberinto[0]),len(laberinto)],vida)
                print(opciones)
                r=encontrarConVida(coordenadasQueso,opciones,estado,coordenadasParedes,[len(laberinto[0]),len(laberinto)],vida)
                if r==False:
                    gui.mensaje("Sin solución","No se encontró un camino para el queso")
                else:
                    v=vida["vidaTotal"]
                    dibujarLaberinto(gui,laberinto,coordenadasParedes,coordenadasRaton,coordenadasQueso,r[0],f"Laberinto | Con vida | Vida usada: {v-r[1]}/{v} puntos")
        if seleccion==2:
            opciones=obtenerOpciones(coordenadasRaton,coordenadasParedes,estado,[len(laberinto[0]),len(laberinto)])
            r=encontrar(coordenadasQueso,opciones,estado,coordenadasParedes,[len(laberinto[0]),len(laberinto)])
            if r==False:
                gui.mensaje("Sin solución","No se encontró un camino para el queso")
            else:
                dibujarLaberinto(gui,laberinto,coordenadasParedes,coordenadasRaton,coordenadasQueso,r,"Laberinto | Unica solución","Salir")
        if seleccion==3:
            respuestas=[]
            opciones=obtenerOpciones(coordenadasRaton,coordenadasParedes,estado,[len(laberinto[0]),len(laberinto)])
            encontrarTodasPosibilidades(coordenadasQueso,opciones,estado,coordenadasParedes,[len(laberinto[0]),len(laberinto)],respuestas)
            if len(respuestas)!=0:
                i=0
                for respuesta in respuestas:
                    i+=1
                    if(i!=len(respuestas)):
                        dibujarLaberinto(gui,laberinto,coordenadasParedes,coordenadasRaton,coordenadasQueso,respuesta,f"Laberinto | Solución {i}/{len(respuestas)}","Siguiente solución")
                    else:
                        dibujarLaberinto(gui,laberinto,coordenadasParedes,coordenadasRaton,coordenadasQueso,respuesta,f"Laberinto | Solución {i}/{len(respuestas)}","Salir")
            else:
                gui.mensaje("Sin solución","No se encontró un camino para el queso")  
            
if __name__=="__main__":
    main()
