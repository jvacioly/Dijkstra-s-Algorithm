import pygame, psycopg2, sys
import math, random
from grafo import Grafo

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

def print_resultado(nodes_anteriores, menor_caminho, node_inicial, target_node):
    caminho = []
    node = target_node

    while node != node_inicial:
        caminho.append(node)
        node = nodes_anteriores[node]
    
    caminho.append(node_inicial)
    caminho = list(map(str, caminho))

    print(f'A menor distância para ir de {node_inicial} à {target_node} é: {menor_caminho[target_node]}.')
    print(' -> '.join(reversed(caminho)))

def draw_grafo(grafo, visited_nodes, node_inicial, target_node):
    # Inicializar o Pygame
    pygame.init()

    # Definir cores
    BLACK = (0, 0, 0)
    BLUE = (0, 0, 255)
    LIGHT_GRAY = (200, 200, 200)
    YELLOW = (255, 255, 0)

    # Configurar a tela
    screen = pygame.display.set_mode((1280, 960))
    pygame.display.set_caption("Visualização do Grafo")
    screen.fill(BLACK)

    # Definir posições dos nós
    pos = {}
    for node in grafo.get_nodes():
        pos[node] = (random.randint(50, 1230), random.randint(50, 910))

    # Desenhar arestas
    for node in grafo.get_nodes():
        for neighbor in grafo.get_outgoing_edges(node):
            pygame.draw.line(screen, LIGHT_GRAY, pos[node], pos[neighbor], 1)

    # Desenhar nós
    for node in grafo.get_nodes():
        color = BLUE
        if node == node_inicial or node == target_node:
            color = YELLOW
        pygame.draw.circle(screen, color, pos[node], 5)
    
    pygame.display.flip()

    # Loop de atualização
    clock = pygame.time.Clock()
    for node in visited_nodes:
        screen.fill(BLACK)
        for node_inner in grafo.get_nodes():
            for neighbor in grafo.get_outgoing_edges(node_inner):
                pygame.draw.line(screen, LIGHT_GRAY, pos[node_inner], pos[neighbor], 1)

        for node_inner in grafo.get_nodes():
            color = BLUE
            if node_inner == node_inicial or node_inner == target_node:
                color = YELLOW
            pygame.draw.circle(screen, color, pos[node_inner], 5)

        pygame.draw.circle(screen, BLUE, pos[node], 5)
        pygame.display.flip()
        clock.tick(1)  # Atualiza a cada segundo

    # Espera até o usuário fechar a janela
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    pygame.quit()

# Obter dados do banco de dados
rows = fetch_data_from_db()
# Construir o grafo a partir dos dados do banco de dados
grafo = build_grafo_from_db_data(rows)

# Definir os nós inicial e alvo
node_inicial = 0  # Altere conforme necessário
target_node = 9  # Altere conforme necessário

# Executar o algoritmo de Dijkstra
nodes_anteriores, menor_caminho, visited_nodes = dijkstra_algorithm(grafo, node_inicial)
# Imprimir o resultado
print_resultado(nodes_anteriores, menor_caminho, node_inicial, target_node)

# Visualizar o grafo
draw_grafo(grafo, visited_nodes, node_inicial, target_node)