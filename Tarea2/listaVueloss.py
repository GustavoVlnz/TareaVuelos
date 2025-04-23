class Nodo:
    def __init__(self, vuelo):
        self.vuelo = vuelo
        self.anterior = None
        self.siguiente = None


class ListaVuelos:
    def __init__(self, session):
        self.cabeza = None
        self.cola = None
        self.size = 0
        self.session = session
        self.pila_undo = []
        self.pila_redo = []

    def registrar_undo(self, accion):
        self.pila_undo.append(accion)
        self.pila_redo.clear() 

    def insertar_al_frente(self, vuelo):
        nuevo_nodo = Nodo(vuelo)
        if self.cabeza is None:
            self.cabeza = self.cola = nuevo_nodo
        else:
            nuevo_nodo.siguiente = self.cabeza
            self.cabeza.anterior = nuevo_nodo
            self.cabeza = nuevo_nodo
        self.size += 1
        self.registrar_undo({"tipo": "insertar", "vuelo": vuelo, "posicion": 0})
        self.session.add(vuelo)
        self.session.commit()

    def insertar_al_final(self, vuelo):
        nuevo_nodo = Nodo(vuelo)
        if self.cola is None:
            self.cabeza = self.cola = nuevo_nodo
        else:
            self.cola.siguiente = nuevo_nodo
            nuevo_nodo.anterior = self.cola
            self.cola = nuevo_nodo
        self.size += 1
        self.registrar_undo({"tipo": "insertar", "vuelo": vuelo, "posicion": self.size - 1})
        self.session.add(vuelo)
        self.session.commit()

    def obtener_primero(self):
        return self.cabeza.vuelo if self.cabeza else None

    def obtener_ultimo(self):
        return self.cola.vuelo if self.cola else None

    def longitud(self):
        return self.size

    def insertar_en_posicion(self, vuelo, posicion):
        if posicion <= 0:
            self.insertar_al_frente(vuelo)
        elif posicion >= self.size:
            self.insertar_al_final(vuelo)
        else:
            nuevo_nodo = Nodo(vuelo)
            actual = self.cabeza
            for _ in range(posicion):
                actual = actual.siguiente
            anterior = actual.anterior

            anterior.siguiente = nuevo_nodo
            nuevo_nodo.anterior = anterior

            nuevo_nodo.siguiente = actual
            actual.anterior = nuevo_nodo
            self.size += 1
            self.registrar_undo({"tipo": "insertar", "vuelo": vuelo, "posicion": posicion})
            self.session.add(vuelo) 
            self.session.commit()

    def extraer_de_posicion(self, posicion):
        if posicion < 0 or posicion >= self.size:
            return None

        if posicion == 0:
            vuelo = self.cabeza.vuelo
            self.cabeza = self.cabeza.siguiente
            if self.cabeza:
                self.cabeza.anterior = None
            else:
                self.cola = None
            self.size -= 1
            self.registrar_undo({"tipo": "eliminar", "vuelo": vuelo, "posicion": posicion})
            return vuelo

        if posicion == self.size - 1:
            vuelo = self.cola.vuelo
            self.cola = self.cola.anterior
            if self.cola:
                self.cola.siguiente = None
            else:
                self.cabeza = None
            self.size -= 1
            self.registrar_undo({"tipo": "eliminar", "vuelo": vuelo, "posicion": posicion})
            return vuelo

        actual = self.cabeza
        for _ in range(posicion):
            actual = actual.siguiente

        vuelo = actual.vuelo
        anterior = actual.anterior
        siguiente = actual.siguiente

        anterior.siguiente = siguiente
        siguiente.anterior = anterior
        self.size -= 1
        self.registrar_undo({"tipo": "eliminar", "vuelo": vuelo, "posicion": posicion})
        self.session.delete(vuelo)
        self.session.commit()
        return vuelo

    def recorrer_lista(self):
        vuelos = []
        actual = self.cabeza
        while actual:
            vuelos.append(actual.vuelo)
            actual = actual.siguiente
        return vuelos

    def mover_vuelo(self, posicion_origen, posicion_destino):
        if posicion_origen < 0 or posicion_origen >= self.size or posicion_destino < 0 or posicion_destino > self.size:
            return None

        vuelo = self.extraer_de_posicion(posicion_origen)
        if vuelo is None:
            return None

        self.insertar_en_posicion(vuelo, posicion_destino)
        self.registrar_undo({
            "tipo": "mover",
            "vuelo": vuelo,
            "posicion_original": posicion_origen,
            "posicion_nueva": posicion_destino
        })
        return vuelo

    def undo(self):
        if not self.pila_undo:
            return None
        accion = self.pila_undo.pop()
        tipo = accion["tipo"]

        if tipo == "insertar":
            self.extraer_de_posicion(accion["posicion"])
            self.pila_redo.append(accion)

        elif tipo == "eliminar":
            self.insertar_en_posicion(accion["vuelo"], accion["posicion"])
            self.pila_redo.append(accion)

        elif tipo == "mover":
            vuelo = self.extraer_de_posicion(accion["posicion_nueva"])
            self.insertar_en_posicion(vuelo, accion["posicion_original"])
            self.pila_redo.append(accion)

        return accion

    def redo(self):
        if not self.pila_redo:
            return None
        accion = self.pila_redo.pop()
        tipo = accion["tipo"]

        if tipo == "insertar":
            self.insertar_en_posicion(accion["vuelo"], accion["posicion"])
            self.pila_undo.append(accion)

        elif tipo == "eliminar":
            self.extraer_de_posicion(accion["posicion"])
            self.pila_undo.append(accion)

        elif tipo == "mover":
            vuelo = self.extraer_de_posicion(accion["posicion_original"])
            self.insertar_en_posicion(vuelo, accion["posicion_nueva"])
            self.pila_undo.append(accion)

        return accion
