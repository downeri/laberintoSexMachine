from copy import deepcopy
from funcionesUnicaSolucion import unica as us

class mejor:
    def encontrarMejorSolucion(self,objetivo,opciones,estado,coordenadasParedes,tamanoLab,respuestas,pasos):
        if objetivo in opciones:
            estado.append(objetivo)
            respuestas[0].append(estado)
            respuestas[1].append(pasos+1)
        elif len(opciones)==0:
            return False
        for opcion in opciones:
            estadoTemp=deepcopy(estado)
            estadoTemp.append(opcion)
            nuevasOpciones=us.obtenerOpciones(opcion,coordenadasParedes,estadoTemp,tamanoLab)
            pasosTemp=pasos+1
            self.encontrarMejorSolucion(self,objetivo,nuevasOpciones,estadoTemp,coordenadasParedes,tamanoLab,respuestas,pasosTemp)
        if len(respuestas[0])==0:
            return False
        return True