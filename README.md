ANÁLISIS TEÓRICO OBLIGATORIO - RED DE TRANSPORTE

1. ESTRUCTURAS DE DATOS UTILIZADAS Y JUSTIFICACIÓN
--------------------------------------------------
Para la implementación de este sistema se han seleccionado estructuras de datos eficientes que cumplen de forma estricta con los requisitos técnicos solicitados en el examen:

* Diccionarios (dict) para la Lista de Adyacencia:
  Se ha utilizado un diccionario dinámico (`self.grafo`) donde las claves son los nombres de las estaciones y los valores son listas de tuplas (destino, minutos).
  - Justificación: Permite añadir estaciones y verificar la existencia de un nodo en tiempo constante O(1). Además, representa el grafo de forma óptima en memoria al tratarse de una red de transporte dispersa (pocas conexiones por estación en comparación con el total de nodos).

* Conjuntos (sets) para Nodos Visitados:
  Tanto en el algoritmo BFS (`estan_conectadas`) como de forma implícita en la lógica de control, se utilizan conjuntos para registrar los nodos ya procesados.
  - Justificación: La búsqueda y la inserción en un conjunto en Python tienen una complejidad media de O(1), superando drásticamente el rendimiento de una lista tradicional O(N) al evitar bucles de verificación lineal.

* Cola de Prioridad (heap con heapq):
  En el algoritmo de Dijkstra (`ruta_mas_rapida`), se utiliza un Min-Heap mediante la librería nativa `heapq`.
  - Justificación: Permite extraer siempre el nodo con la menor distancia acumulada en tiempo logarítmico O(log V), lo cual es el núcleo de la eficiencia del algoritmo frente a una búsqueda lineal.


2. COMPLEJIDAD TEMPORAL DE LAS OPERACIONES
------------------------------------------
A continuación se detalla el coste computacional de las funciones principales utilizando la notación Big-O (donde V representa el número de Vértices o estaciones, y E el número de Aristas o conexiones):

* Añadir Conexión (`anadir_conexion`):
  - Complejidad: O(K), donde K es el número de vecinos de la estación de origen.
  - Análisis: Validar la existencia de las estaciones toma O(1) gracias al diccionario. Sin embargo, para evitar conexiones duplicadas, recorremos de forma lineal la lista de vecinos del nodo origen para comprobar si el destino ya existe. En el peor de los casos (un nodo central "hub" conectado a casi toda la red), esta operación puede llegar a aproximarse a O(V).

* Algoritmo de Dijkstra (`ruta_mas_rapida`):
  - Complejidad: O((V + E) log V)
  - Análisis: En el peor de los casos, cada vértice y cada arista se evalúan. Insertar y extraer elementos del Min-Heap toma un tiempo de O(log V). Al usar la lista de adyacencia combinada con la cola de prioridad de `heapq`, el rendimiento está optimizado para redes de transporte de gran escala.

* Comprobación de Conectividad mediante BFS (`estan_conectadas`):
  - Complejidad: O(V + E)
  - Análisis: El algoritmo de búsqueda en anchura explora sistemáticamente todos los nodos y aristas accesibles desde el origen. Como cada nodo se añade a la cola y se marca como visitado una sola vez, y cada arista se recorre un número fijo de veces, la complejidad es estrictamente lineal respecto al tamaño del grafo.


3. COMPLEJIDAD ESPACIAL DEL GRAFO
---------------------------------
* Complejidad: O(V + E)
* Análisis: El espacio ocupado en memoria por la lista de adyacencia crece de manera proporcional al número de estaciones (V) más el número de conexiones bidireccionales (2 * E). Es la representación más eficiente en espacio para este tipo de problemas, a diferencia de una matriz de adyacencia que requeriría un espacio fijo de O(V^2) independientemente de las conexiones reales.


4. PROPUESTAS DE MEJORA Y OPTIMIZACIÓN
--------------------------------------
Revisando la implementación actual, se identifican las siguientes áreas de mejora para futuras versiones del software:

1. Optimización de Duplicados en Conexiones: En lugar de almacenar los vecinos en una lista `[]` (lo que obliga a una búsqueda lineal O(K) para evitar duplicados), se podría cambiar el valor del diccionario de adyacencia a otro diccionario interno o a un conjunto de tuplas. Esto reduciría la complejidad de `anadir_conexion` a un óptimo O(1).

2. Manejo Eficiente de Archivos (Persistencia): Actualmente el programa carga/guarda todo el JSON de golpe sustituyendo el grafo en memoria. Sería ideal implementar una sincronización incremental o añadir una base de datos ligera (`sqlite3`) para no saturar la memoria RAM si la red de transporte escala a millones de estaciones.

3. Modularización y Separación de Capas: La lógica de la interfaz de usuario (el bucle `while` y los `input()` del menú) está mezclada directamente con la ejecución del script en el mismo archivo. Separar la clase `RedTransporte` en un módulo de lógica de negocio independiente y dejar el menú en un archivo `main.py` mejoraría drásticamente la mantenibilidad y escalabilidad del código
