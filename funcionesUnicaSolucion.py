from copy import deepcopy

class unica:
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

    def encontrar(self,objetivo,opciones,estado,coordenadasParedes,tamanoLab):
        if objetivo in opciones:
            estadoTemp=deepcopy(estado)
            estadoTemp.append(objetivo)
            return estadoTemp
        elif len(opciones)==0:
            return False
        for opcion in opciones:
            estadoTemp=deepcopy(estado)
            estadoTemp.append(opcion)
            nuevasOpciones=self.obtenerOpciones(opcion,coordenadasParedes,estadoTemp,tamanoLab)
            r=self.encontrar(self,objetivo,nuevasOpciones,estadoTemp,coordenadasParedes,tamanoLab)
            if r!=False:
                return r
        return False