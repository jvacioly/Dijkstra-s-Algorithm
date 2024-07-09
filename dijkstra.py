import sys
import psycopg2
import networkx as nx
import matplotlib.pyplot as plt
import seaborn as sns
from grafo import Grafo
import matplotlib.animation as animation

# Função para buscar dados do banco de dados
def fetch_data_from_db():
    db_name = 'postgres'
    db_user = 'postgres'
    db_password = '1234'
    db_host = 'localhost'
    db_port = '5432'

    try:
        connection = psycopg2.connect(
            dbname=db_name,
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port
        )
        cursor = connection.cursor()
        cursor.execute('SELECT vertice1, vertice2, peso FROM grafo')
        rows = cursor.fetchall()
        return rows
    except (Exception, psycopg2.Error) as error:
        print("Erro ao conectar ao PostgreSQL", error)
    finally:
        if connection:
            cursor.close()
            connection.close()

# Função para construir o grafo a partir dos dados do banco de dados
def build_grafo_from_db_data(rows):
    init_grafo = {}
    nodes = set()
    for vertice1, vertice2, peso in rows:
        if vertice1 not in init_grafo:
            init_grafo[vertice1] = {}
        if vertice2 not in init_grafo:
            init_grafo[vertice2] = {}
        init_grafo[vertice1][vertice2] = peso
        nodes.update([vertice1, vertice2])
    nodes = list(nodes)
    return Grafo(nodes, init_grafo)

# Algoritmo de Dijkstra
def dijkstra_algorithm(grafo, node_inicial):
    nodes_nao_visitados = list(grafo.get_nodes())
    menor_caminho = {}
    nodes_anteriores = {}
    max_value = sys.maxsize
    for node in nodes_nao_visitados:
        menor_caminho[node] = max_value
    menor_caminho[node_inicial] = 0

    visited_nodes = []

    while nodes_nao_visitados:
        min_node_atual = None
        for node in nodes_nao_visitados:
            if min_node_atual is None:
                min_node_atual = node
            elif menor_caminho[node] < menor_caminho[min_node_atual]:
                min_node_atual = node
        
        vizinhos = grafo.get_outgoing_edges(min_node_atual)
        for vizinho in vizinhos:
            valor_provisorio = menor_caminho[min_node_atual] + grafo.value(min_node_atual, vizinho)
            if valor_provisorio < menor_caminho[vizinho]:
                menor_caminho[vizinho] = valor_provisorio
                nodes_anteriores[vizinho] = min_node_atual

        visited_nodes.append(min_node_atual)
        nodes_nao_visitados.remove(min_node_atual)
    
    return nodes_anteriores, menor_caminho, visited_nodes

# Função para imprimir o resultado do algoritmo de Dijkstra
def print_resultado(nodes_anteriores, menor_caminho, node_inicial, target_node):
    caminho = []
    node = target_node

    while node != node_inicial:
        caminho.append(node)
        node = nodes_anteriores[node]
    
    caminho.append(node_inicial)
    caminho = list(map(int, reversed(caminho)))

    print(f'A menor distância para ir de {node_inicial} à {target_node} é: {menor_caminho[target_node]}.')
    print(' -> '.join(map(str, caminho)))
    return caminho

# Função para desenhar o grafo utilizando Seaborn
def draw_graph(grafo, caminho, node_inicial, target_node, visited_nodes):
    G = nx.Graph()
    for node in grafo.get_nodes():
        G.add_node(node)
    for node in grafo.get_nodes():
        for neighbor in grafo.get_outgoing_edges(node):
            G.add_edge(node, neighbor, weight=grafo.value(node, neighbor))

    fig, ax = plt.subplots(figsize=(16, 12))
    pos = nx.spring_layout(G)

    def update(num):
        ax.clear()
        # Desenhando as arestas em preto
        nx.draw_networkx_edges(G, pos, edge_color='black', width=0.5, ax=ax)

        # Desenhando os nós
        node_colors = ['green' if node == node_inicial or node == target_node else 'red' for node in G.nodes()]
        nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=100, ax=ax)

        # Desenhando os nós visitados até agora em preto
        if num < len(visited_nodes):
            nx.draw_networkx_nodes(G, pos, nodelist=[node for node in visited_nodes[:num] if node != node_inicial], node_color='black', node_size=100, ax=ax)
        else:
            # Desenhando o caminho final em verde
            step = num - len(visited_nodes)
            if step > 0:
                caminho_edges = [(caminho[i], caminho[i+1]) for i in range(step) if i < len(caminho) - 1]
                nx.draw_networkx_edges(G, pos, edgelist=caminho_edges, edge_color='green', width=2, ax=ax)
                nx.draw_networkx_nodes(G, pos, nodelist=caminho[:step], node_color='green', node_size=200, ax=ax)

        # Desenhando os labels dos nós
        nx.draw_networkx_labels(G, pos, font_size=8, font_color='white', ax=ax)

        ax.set_title('Visualização do Grafo')
        ax.axis('off')

    ani = animation.FuncAnimation(fig, update, frames=len(visited_nodes) + len(caminho), interval=250, repeat=False)
    plt.show()

# Carregar os dados do banco de dados
rows = fetch_data_from_db()

# Construir o grafo
grafo = build_grafo_from_db_data(rows)

# Definir o nó inicial e o nó alvo
node_inicial = 1
target_node = 24  

# Executar o algoritmo de Dijkstra
nodes_anteriores, menor_caminho, visited_nodes = dijkstra_algorithm(grafo, node_inicial)

# Imprimir o resultado e obter o caminho
caminho = print_resultado(nodes_anteriores, menor_caminho, node_inicial, target_node)

# Desenhar o grafo com a animação
draw_graph(grafo, caminho, node_inicial, target_node, visited_nodes)
