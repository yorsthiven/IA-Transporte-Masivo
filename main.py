import heapq

# 1. BASE DE CONOCIMIENTO (Representación del mundo)
# Diccionario de conexiones: 'Origen': [('Destino', tiempo_minutos), ...]
estaciones = {
    'Portal Norte': [('Calle 100', 15), ('Suba Calle 100', 10)],
    'Calle 100': [('Portal Norte', 15), ('Héroes', 5), ('Ricaurte', 20)],
    'Héroes': [('Calle 100', 5), ('Calle 26', 10)],
    'Suba Calle 100': [('Portal Norte', 10), ('Ricaurte', 25)],
    'Ricaurte': [('Calle 100', 20), ('Suba Calle 100', 25), ('Jiménez', 5), ('Portal Sur', 30)],
    'Calle 26': [('Héroes', 10), ('Jiménez', 5)],
    'Jiménez': [('Ricaurte', 5), ('Calle 26', 5), ('Portal Américas', 25)],
    'Portal Sur': [('Ricaurte', 30)],
    'Portal Américas': [('Jiménez', 25)]
}

# 2. HEURÍSTICA (Conocimiento experto)
# Coordenadas aproximadas (X, Y) para calcular distancia en línea recta
# Esto hace que el sistema sea "Inteligente" según el Capítulo 9 de Benítez
coordenadas = {
    'Portal Norte': (0, 10),
    'Calle 100': (0, 7),
    'Suba Calle 100': (-2, 7),
    'Héroes': (0, 5),
    'Calle 26': (0, 2),
    'Ricaurte': (-1, 0),
    'Jiménez': (1, 0),
    'Portal Sur': (-2, -10),
    'Portal Américas': (-5, 0)
}

def calcular_heuristica(actual, destino):
    # Distancia Euclidiana simple entre puntos
    (x1, y1) = coordenadas[actual]
    (x2, y2) = coordenadas[destino]
    return ((x1 - x2)**2 + (y1 - y2)**2)**0.5

# 3. ALGORITMO DE BÚSQUEDA HEURÍSTICA (A*)
def busqueda_a_estrella(inicio, destino):
    cola_prioridad = [(0, inicio)] # (prioridad, nodo_actual)
    rastreo = {inicio: None}
    costo_acumulado = {inicio: 0}

    while cola_prioridad:
        _, actual = heapq.heappop(cola_prioridad)

        if actual == destino:
            break

        for vecino, peso in estaciones.get(actual, []):
            nuevo_costo = costo_acumulado[actual] + peso
            if vecino not in costo_acumulado or nuevo_costo < costo_acumulado[vecino]:
                costo_acumulado[vecino] = nuevo_costo
                # f(n) = g(n) + h(n)
                prioridad = nuevo_costo + calcular_heuristica(vecino, destino)
                heapq.heappush(cola_prioridad, (prioridad, vecino))
                rastreo[vecino] = actual

    return reconstruir_ruta(rastreo, inicio, destino), costo_acumulado.get(destino, 0)

def reconstruir_ruta(rastreo, inicio, destino):
    ruta = []
    actual = destino
    while actual is not None:
        ruta.append(actual)
        actual = rastreo[actual]
    ruta.reverse()
    return ruta

# 4. EJECUCIÓN DE PRUEBA
if __name__ == "__main__":
    origen = "Portal Norte"
    fin = "Jiménez"
    
    resultado, tiempo = busqueda_a_estrella(origen, fin)
    
    print(f"--- SISTEMA INTELIGENTE DE RUTAS ---")
    print(f"Origen: {origen} -> Destino: {fin}")
    print(f"Mejor ruta encontrada: {' -> '.join(resultado)}")
    print(f"Tiempo estimado: {tiempo} minutos")