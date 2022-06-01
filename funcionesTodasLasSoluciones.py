from copy import deepcopy
from funcionesUnicaSolucion import unica as us

class todas:
    def encontrarTodasPosibilidades(self,objetivo,opciones,estado,coordenadasParedes,tamanoLab,respuestas):
        if objetivo in opciones:
            estado.append(objetivo)
            respuestas.append(estado)
        elif len(opciones)==0:
            return False
        for opcion in opciones:
            estadoTemp=deepcopy(estado)
            estadoTemp.append(opcion)
            nuevasOpciones=us.obtenerOpciones(opcion,coordenadasParedes,estadoTemp,tamanoLab)
            self.encontrarTodasPosibilidades(self,objetivo,nuevasOpciones,estadoTemp,coordenadasParedes,tamanoLab,respuestas)
        if len(respuestas)==0:
            return False
        return True