import json
import heapq
import os

import networkx as nx
import matplotlib.pyplot as plt


class RedTransporte:

    def __init__(self):

        # Lista de adyacencia
        # {
        #   "A": [("B", 5), ("C", 10)]
        # }

        self.grafo = {}

    # =====================================================
    # AÑADIR ESTACIÓN
    # =====================================================

    def anadir_estacion(self, estacion):

        if estacion in self.grafo:
            print("La estación ya existe.")
            return

        self.grafo[estacion] = []

        print("Estación añadida correctamente.")

    # =====================================================
    # AÑADIR CONEXIÓN
    # =====================================================

    def anadir_conexion(self, origen, destino, minutos):

        # Validar estaciones

        if origen not in self.grafo:
            print(f"La estación {origen} no existe.")
            return

        if destino not in self.grafo:
            print(f"La estación {destino} no existe.")
            return

        # Validar tiempo

        if minutos <= 0:
            print("El tiempo debe ser positivo.")
            return

        # Evitar conexiones duplicadas

        for vecino, _ in self.grafo[origen]:

            if vecino == destino:
                print("La conexión ya existe.")
                return

        # Añadir conexión (grafo no dirigido)

        self.grafo[origen].append((destino, minutos))
        self.grafo[destino].append((origen, minutos))

        print("Conexión añadida correctamente.")

    # =====================================================
    # MOSTRAR RED COMO GRAFO
    # =====================================================

    def mostrar_red(self):

        if not self.grafo:
            print("La red está vacía.")
            return

        # Crear grafo

        G = nx.Graph()

        # Añadir nodos y aristas

        for estacion in self.grafo:

            G.add_node(estacion)

            for vecino, minutos in self.grafo[estacion]:

                G.add_edge(estacion, vecino, weight=minutos)

        # Layout del grafo

        pos = nx.kamada_kawai_layout(G)

        # Dibujar nodos y conexiones

        nx.draw(
            G,
            pos,
            with_labels=True,
            node_size=3000,
            font_size=10
        )

        # Etiquetas de pesos

        etiquetas = nx.get_edge_attributes(G, "weight")

        nx.draw_networkx_edge_labels(
            G,
            pos,
            edge_labels=etiquetas
        )

        plt.title("Red de Transporte")
        plt.show()

    # =====================================================
    # DIJKSTRA - RUTA MÁS RÁPIDA
    # =====================================================

    def ruta_mas_rapida(self, inicio, fin):

        if inicio not in self.grafo:
            print("La estación de inicio no existe.")
            return

        if fin not in self.grafo:
            print("La estación destino no existe.")
            return

        # Distancias

        distancias = {}

        for estacion in self.grafo:
            distancias[estacion] = float("inf")

        distancias[inicio] = 0

        # Diccionario para reconstruir camino

        anteriores = {}

        # Heap de prioridad

        heap = [(0, inicio)]

        while heap:

            distancia_actual, estacion_actual = heapq.heappop(heap)

            # Si llegamos al destino

            if estacion_actual == fin:
                break

            # Revisar vecinos

            for vecino, minutos in self.grafo[estacion_actual]:

                nueva_distancia = distancia_actual + minutos

                if nueva_distancia < distancias[vecino]:

                    distancias[vecino] = nueva_distancia
                    anteriores[vecino] = estacion_actual

                    heapq.heappush(
                        heap,
                        (nueva_distancia, vecino)
                    )

        # Si no existe camino

        if distancias[fin] == float("inf"):
            print("No existe una ruta.")
            return

        # Reconstruir camino

        camino = []

        actual = fin

        while actual != inicio:

            camino.append(actual)
            actual = anteriores[actual]

        camino.append(inicio)

        camino.reverse()

        print("\n===== RUTA MÁS RÁPIDA =====")
        print(" -> ".join(camino))
        print(f"Tiempo total: {distancias[fin]} minutos")

    # =====================================================
    # BFS - CONECTIVIDAD Y CAMINO
    # =====================================================

    def estan_conectadas(self, origen, destino):

        if origen not in self.grafo:
            print("La estación origen no existe.")
            return

        if destino not in self.grafo:
            print("La estación destino no existe.")
            return

        # BFS

        visitados = set()

        cola = [origen]

        # Para reconstruir camino

        anteriores = {}

        while cola:

            actual = cola.pop(0)

            # Si llegamos al destino

            if actual == destino:

                # Reconstruir camino

                camino = []

                nodo = destino

                while nodo != origen:

                    camino.append(nodo)
                    nodo = anteriores[nodo]

                camino.append(origen)

                camino.reverse()

                print("\nSí, las estaciones están conectadas.")
                print("Debes pasar por:")

                print(" -> ".join(camino))

                return

            if actual not in visitados:

                visitados.add(actual)

                for vecino, _ in self.grafo[actual]:

                    if vecino not in visitados:

                        # Guardar de dónde venimos

                        if vecino not in anteriores:
                            anteriores[vecino] = actual

                        cola.append(vecino)

        print("No están conectadas.")

    # =====================================================
    # GUARDAR JSON
    # =====================================================

    def guardar_json(self, archivo):

        datos = []

        conexiones_guardadas = set()

        for origen in self.grafo:

            for destino, minutos in self.grafo[origen]:

                # Evitar duplicados

                clave = tuple(sorted([origen, destino]))

                if clave not in conexiones_guardadas:

                    datos.append({
                        "origen": origen,
                        "destino": destino,
                        "minutos": minutos
                    })

                    conexiones_guardadas.add(clave)

        with open(archivo, "w", encoding="utf-8") as f:

            json.dump(
                datos,
                f,
                indent=4,
                ensure_ascii=False
            )

        print("Archivo JSON guardado correctamente.")

    # =====================================================
    # CARGAR JSON
    # =====================================================

    def cargar_json(self, archivo):

        if not os.path.exists(archivo):
            print("El archivo no existe.")
            return

        with open(archivo, "r", encoding="utf-8") as f:

            datos = json.load(f)

        self.grafo = {}

        # Crear estaciones

        for conexion in datos:

            origen = conexion["origen"]
            destino = conexion["destino"]

            if origen not in self.grafo:
                self.grafo[origen] = []

            if destino not in self.grafo:
                self.grafo[destino] = []

        # Crear conexiones

        for conexion in datos:

            origen = conexion["origen"]
            destino = conexion["destino"]
            minutos = conexion["minutos"]

            self.grafo[origen].append(
                (destino, minutos)
            )

            self.grafo[destino].append(
                (origen, minutos)
            )

        print("Archivo JSON cargado correctamente.")

    # =====================================================
    # BONUS - ESTACIÓN HUB
    # =====================================================

    def estacion_hub(self):

        if not self.grafo:
            print("La red está vacía.")
            return

        hub = max(
            self.grafo,
            key=lambda x: len(self.grafo[x])
        )

        print("\n===== ESTACIÓN HUB =====")
        print(f"Estación: {hub}")

        print(
            f"Número de conexiones: "
            f"{len(self.grafo[hub])}"
        )


# =====================================================
# MENÚ
# =====================================================

def menu():

    red = RedTransporte()

    while True:

        print("\n========= MENÚ =========")
        print("1. Cargar red desde archivo JSON")
        print("2. Añadir estación")
        print("3. Añadir conexión")
        print("4. Ver red de paradas como grafo")
        print("5. Ruta más rápida entre 2 estaciones")
        print("6. Están conectadas estas estaciones?")
        print("7. Ver estación HUB")
        print("8. Guardar en JSON")
        print("9. Salir")

        opcion = input("\nSeleccione una opción: ")

        try:

            # =================================================
            # CARGAR JSON
            # =================================================

            if opcion == "1":

                archivo = input(
                    "Nombre del archivo JSON: "
                )

                red.cargar_json(archivo)

            # =================================================
            # AÑADIR ESTACIÓN
            # =================================================

            elif opcion == "2":

                estacion = input(
                    "Nombre de la estación: "
                )

                red.anadir_estacion(estacion)

            # =================================================
            # AÑADIR CONEXIÓN
            # =================================================

            elif opcion == "3":

                origen = input("Origen: ")
                destino = input("Destino: ")

                minutos = int(
                    input("Minutos: ")
                )

                red.anadir_conexion(
                    origen,
                    destino,
                    minutos
                )

            # =================================================
            # MOSTRAR GRAFO
            # =================================================

            elif opcion == "4":

                red.mostrar_red()

            # =================================================
            # DIJKSTRA
            # =================================================

            elif opcion == "5":

                inicio = input("Inicio: ")
                fin = input("Destino: ")

                red.ruta_mas_rapida(
                    inicio,
                    fin
                )

            # =================================================
            # BFS
            # =================================================

            elif opcion == "6":

                origen = input("Origen: ")
                destino = input("Destino: ")

                red.estan_conectadas(
                    origen,
                    destino
                )

            # =================================================
            # HUB
            # =================================================

            elif opcion == "7":

                red.estacion_hub()

            # =================================================
            # GUARDAR JSON
            # =================================================

            elif opcion == "8":

                archivo = input(
                    "Nombre del archivo JSON: "
                )

                red.guardar_json(archivo)

            # =================================================
            # SALIR
            # =================================================

            elif opcion == "9":

                print("Saliendo del programa...")
                break

            else:
                print("Opción inválida.")

        except ValueError:

            print("Error: introduce valores válidos.")

        except Exception as e:

            print("Ha ocurrido un error:")
            print(e)


# =====================================================
# EJECUCIÓN
# =====================================================

menu()