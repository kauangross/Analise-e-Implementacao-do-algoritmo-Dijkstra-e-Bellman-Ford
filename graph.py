#Julia Andreis, Kauan Gross e Tobias Klein

import heapq
import time

class Graph:
    def __init__(self, graph: dict | None = None):
        # NÃO usar dict{} como default argument (mutável)
        self.graph = graph if graph is not None else {}
        self._cache_dijkstra = {}  # guarda resultados por (source, algoritmo)
        self._cache_bellman = {}  # guarda resultados por (source, algoritmo)

    def add_edge(self, node1, node2, weight, undirected: bool = False):
        if node1 not in self.graph:
            self.graph[node1] = {}
        self.graph[node1][node2] = weight
        if undirected:
            if node2 not in self.graph:
                self.graph[node2] = {}
            self.graph[node2][node1] = weight

    def dijkstra(self, source: str):
        # garante que todos os nós (keys e vizinhos) estejam no conjunto de nós
        nodes = set(self.graph.keys())
        for nbrs in self.graph.values():
            nodes.update(nbrs.keys())

        if source not in nodes:
            raise ValueError(f"Source {source!r} não existe no grafo.")

        # inicializa distâncias e predecessor (para reconstruir caminhos)
        distances = {node: float("inf") for node in nodes}
        prev = {node: None for node in nodes}
        distances[source] = 0

        visited = set()  # <---- conjunto para marcar nós finalizados

        pq = [(0, source)]
        while pq:
            current_dist, current_node = heapq.heappop(pq)

            # descarta entradas antigas na heap
            if current_node in visited:
                continue
            visited.add(current_node) # marca o nó como visitado

            # usa get para evitar KeyError caso current_node não tenha arestas
            for neighbor, weight in self.graph.get(current_node, {}).items():
                new_dist = current_dist + weight

                if new_dist < distances[neighbor]:
                    distances[neighbor] = new_dist
                    prev[neighbor] = current_node
                    heapq.heappush(pq, (new_dist, neighbor))

        self._cache_dijkstra = (distances, prev)
        return distances, prev
    
    def bellman_ford(self, source: str):
        # garante que todos os nós (keys e vizinhos) estejam no conjunto de nós
        nodes = set(self.graph.keys())
        for nbrs in self.graph.values():
            nodes.update(nbrs.keys())

        if source not in nodes:
            raise ValueError(f"Source {source!r} não existe no grafo.")

        # inicializa distâncias e predecessor (para reconstruir caminhos)
        distances = {node: float("inf") for node in nodes}
        prev = {node: None for node in nodes}
        distances[source] = 0

        for nbrs in range(len(nodes) - 1):
            updated = False
            for u in self.graph:
                for v, weight in self.graph[u].items():
                    if distances[u] + weight < distances[v]:
                        distances[v] = distances[u] + weight
                        prev[v] = u
                        updated = True
            
            # Se nenhuma aresta foi relaxada, pode parar antes
            if not updated:
                break

        # Verifica ciclos de peso negativo
        for u in self.graph:
            for v, weight in self.graph[u].items():
                if distances[u] + weight < distances[v]:
                    raise ValueError("O grafo contém um ciclo de peso negativo.")


        self._cache_bellman = (distances, prev)
        return distances, prev

    def shortest_path(self, source: str, target: str, algorithm: str):
        if algorithm == "dijkstra":
            distances, prev = self.dijkstra(source)
        elif algorithm == "bellman-ford":
            distances, prev = self.bellman_ford(source)

        path = []
        cur = target

        # Se não existe caminho, devolve caminho vazio
        if distances[target] == float("inf"):
            return [], float("inf")
        
        while cur is not None:
            path.append(cur)
            cur = prev[cur]
        
        path.reverse()
        
        return path, distances[target]
    
def graph1():
    return Graph({
        "A": {"B": 4, "C": 2, "F": 40},
        "C": {"B": 2, "C": 3},
        "B": {"D": -3},
        "D": {},
        "F": {"B": -40}
    })

def graph2():
    return Graph({
        "A": {"B": 4, "C": 2},
        "C": {"B": 2, "D": 3},
        "B": {"D": 3},
        "D": {}
    })

def graph3() -> "Graph":
    g = Graph()
    g.add_edge("A", "B", 2, undirected=True)
    g.add_edge("A", "D", 15, undirected=True)
    g.add_edge("B", "C", 3, undirected=True)
    g.add_edge("C", "D", 4, undirected=True)
    g.graph["F"] = {}  # nó isolado
    return g

def graphTestTime() -> "Graph":
    return Graph({
        "A": {"B": 2, "C": 5, "D": 3},
        "B": {"A": 2, "E": 3, "F": 4},
        "C": {"A": 5, "F": 2, "G": 6},
        "D": {"A": 3, "G": 2, "H": 4},
        "E": {"B": 3, "I": 5, "J": 2},
        "F": {"B": 4, "C": 2, "J": 3, "K": 4},
        "G": {"C": 6, "D": 2, "K": 1, "L": 3},
        "H": {"D": 4, "L": 2, "M": 5},
        "I": {"E": 5, "M": 3, "N": 4},
        "J": {"E": 2, "F": 3, "N": 2, "O": 4},
        "K": {"F": 4, "G": 1, "O": 3, "P": 2},
        "L": {"G": 3, "H": 2, "P": 4, "Q": 3},
        "M": {"H": 5, "I": 3, "Q": 2, "R": 4},
        "N": {"I": 4, "J": 2, "R": 3, "S": 5},
        "O": {"J": 4, "K": 3, "S": 2, "T": 4},
        "P": {"K": 2, "L": 4, "T": 3, "U": 5},
        "Q": {"L": 3, "M": 2, "U": 2, "V": 4},
        "R": {"M": 4, "N": 3, "V": 3, "W": 2},
        "S": {"N": 5, "O": 2, "W": 3, "X": 4},
        "T": {"O": 4, "P": 3, "X": 2, "Y": 5},
        "U": {"P": 5, "Q": 2, "Y": 3, "Z": 4},
        "V": {"Q": 4, "R": 3, "Z": 2},
        "W": {"R": 2, "S": 3, "Z": 3},
        "X": {"S": 4, "T": 2, "Z": 3},
        "Y": {"T": 5, "U": 3, "Z": 2},
        "Z": {}
    })

def test_dijkstra(graph):
    distances, _ = graph.dijkstra("A")
    print("Distâncias mínimas a partir do nó A:")
    for node in sorted(distances):
        d = distances[node]
        print(f"A → {node}: {d:.2f}" if d < float("inf") else f"A → {node}: ∞")

    path, dist = graph.shortest_path("A", "D", "dijkstra")
    print()
    if path:
        print(f"Caminho mínimo A → D: {' -> '.join(path)} (distância = {dist:.2f})")
    else:
        print("Não há caminho de A até D.")

def test_bellman_ford_(graph):
    # Teste do Bellman-Ford
    distances, _ = graph.bellman_ford("A")

    print("Distâncias mínimas a partir do nó A:")
    for node in sorted(distances):
        d = distances[node]
        print(f"A → {node}: {d:.2f}" if d < float("inf") else f"A → {node}: ∞")

    path, dist = graph.shortest_path("A", "D", "bellman-ford")
    print()
    if path:
        print(f"Caminho mínimo A → D: {' -> '.join(path)} (distância = {dist:.2f})")
    else:
        print("Não há caminho de A até D.")


def teste_dijkstra_com_armadilha(graph: "Graph"):
    print("\n--- TESTE DIJKSTRA ---")

    source = "A"
    target = "D"

    distances, _ = graph.dijkstra(source)

    print(f"Distâncias mínimas a partir do nó {source}:")
    for node in sorted(distances):
        d = distances[node]
        print(f"{source} → {node}: {d:.2f}" if d < float("inf") else f"{source} → {node}: ∞")

    # Caminho A → D
    path, dist = graph.shortest_path(source, target, "dijkstra")
    print()
    if path:
        print(f"Caminho encontrado: {' -> '.join(path)} (distância = {dist:.2f})")
        if dist == 9:
            print("✅ Resultado CORRETO (evitou caminho direto mais caro).")
        else:
            print("❌ Resultado INCORRETO.")
    else:
        print("❌ Caminho não encontrado.")

    # Nó isolado
    print()
    path_iso, _ = graph.shortest_path(source, "F", "dijkstra")
    print(f"Procurando caminho de {source} para F (nó isolado)")
    if not path_iso:
        print("✅ Caminho não encontrado, como esperado.")
    else:
        print("❌ Resultado INCORRETO (achou caminho onde não existe).")

def teste_bellman_ford_com_armadilha(graph: "Graph"):
    print("\n--- TESTE BELLMAN-FORD ---")

    source = "A"
    target = "D"

    distances, _ = graph.bellman_ford(source)

    print(f"Distâncias mínimas a partir do nó {source}:")
    for node in sorted(distances):
        d = distances[node]
        print(f"{source} → {node}: {d:.2f}" if d < float("inf") else f"{source} → {node}: ∞")

    # Caminho A → D
    path, dist = graph.shortest_path(source, target, "bellman-ford")
    print()
    if path:
        print(f"Caminho encontrado: {' -> '.join(path)} (distância = {dist:.2f})")
        if dist == 9:
            print("✅ Resultado CORRETO (encontrou o menor caminho).")
        else:
            print("❌ Resultado INCORRETO.")
    else:
        print("❌ Caminho não encontrado.")

    # Nó isolado
    print()
    path_iso, _ = graph.shortest_path(source, "F", "bellman-ford")
    print(f"Procurando caminho de {source} para F (nó isolado)")
    if not path_iso:
        print("✅ Caminho não encontrado, como esperado.")
    else:
        print("❌ Resultado INCORRETO (achou caminho onde não existe).")

def benchmark():
    graph = graphTestTime()

    # --- Teste Dijkstra ---
    start = time.perf_counter()
    test_dijkstra(graph)
    end = time.perf_counter()
    dijkstra_time = (end - start) * 1000

    # --- Teste Bellman-Ford ---
    start = time.perf_counter()
    test_bellman_ford_(graph)
    end = time.perf_counter()
    bellman_time = (end - start) * 1000

    print(f"Dijkstra: {dijkstra_time:.3f} ms")
    print(f"Bellman-Ford: {bellman_time:.3f} ms")

def main():
    print("\n----------------------------------\n----------Teste Dijkstra com peso negativo - deve falhar:----------")
    test_dijkstra(graph1())
    print("\n----------------------------------\n----------Teste Bellman-Ford com peso negativo - deve funcionar:----------")
    test_bellman_ford_(graph1())

    print('\n----------------------------------\n----------Teste Dijkstra e Bellman-Ford com armadilha:----------')
    teste_dijkstra_com_armadilha(graph3())
    teste_bellman_ford_com_armadilha(graph3())
    
    print("\n\nBenchmark\n")
    for _ in range(3):
        benchmark()


if __name__ == "__main__":
    main()