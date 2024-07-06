import sys
from grafo import Grafo

def dijkstra_algorithm(grafo, node_inicial):
    nodes_nao_visitados = list(grafo.get_nodes())
    menor_caminho = {}
    nodes_anteriores = {}
    max_value = sys.maxsize
    for node in nodes_nao_visitados:
        menor_caminho[node] = max_value
    menor_caminho[node_inicial] = 0

    while nodes_nao_visitados:
        min_node_atual = None
        for node in nodes_nao_visitados:
            if min_node_atual == None:
                min_node_atual = node
            elif menor_caminho[node] < menor_caminho[min_node_atual]:
                min_node_atual = node
        
        vizinhos = grafo.get_outgoing_edges(min_node_atual)
        for vizinho in vizinhos:
            valor_provisorio = menor_caminho[min_node_atual] + grafo.value(min_node_atual, vizinho)
            if valor_provisorio < menor_caminho[vizinho]:
                menor_caminho[vizinho] = valor_provisorio
                nodes_anteriores[vizinho] = min_node_atual

        nodes_nao_visitados.remove(min_node_atual)
    
    return nodes_anteriores, menor_caminho

def print_resultado(nodes_anteriores, menor_caminho, node_inicial, target_node):
    caminho = []
    node = target_node

    while node != node_inicial:
        caminho.append(node)
        node = nodes_anteriores[node]
    
    caminho.append(node_inicial)

    print(f'A menor distância para ir de {node_inicial} à {target_node} é: {menor_caminho[target_node]}.')
    print(' -> '.join(reversed(caminho)))


# Definir o Grafo e chamar as funções:
nodes = ["Reykjavik", "Oslo", "Moscow", "London", "Rome", "Berlin", "Belgrade", "Athens"]

init_grafo = {}
for node in nodes:
    init_grafo[node] = {}
   
init_grafo["Reykjavik"]["Oslo"] = 5
init_grafo["Reykjavik"]["London"] = 4
init_grafo["Oslo"]["Berlin"] = 1
init_grafo["Oslo"]["Moscow"] = 3
init_grafo["Moscow"]["Belgrade"] = 5
init_grafo["Moscow"]["Athens"] = 4
init_grafo["Athens"]["Belgrade"] = 1
init_grafo["Rome"]["Berlin"] = 2
init_grafo["Rome"]["Athens"] = 2

grafo = Grafo(nodes, init_grafo)
node_inicial = 'Reykjavik'
target_node = 'Belgrade'
nodes_anteriores, menor_caminho = dijkstra_algorithm(grafo, node_inicial)
print_resultado(nodes_anteriores, menor_caminho, node_inicial, target_node)