from copy import deepcopy


class fvida:
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

    def encontrarConVida(self,objetivo,opciones,estado,coordenadasParedes,tamanoLab,vida):
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
            nuevasOpciones=self.obtenerOpcionesVida(opcion,coordenadasParedes,estadoTemp,tamanoLab,vidaTemp)
            r=self.encontrarConVida(self,objetivo,nuevasOpciones,estadoTemp,coordenadasParedes,tamanoLab,vidaTemp)
            if r!=False:
                return r
            i+=1
        return False