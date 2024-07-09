import sys, psycopg2
from grafo import Grafo

# Construindo o Grafo
def fetch_data_from_db():
    # Parâmetros de conexão ao banco de dados
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

# Busca da melhor Rota
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
    caminho = list(map(str, caminho))


    print(f'A menor distância para ir de {node_inicial} à {target_node} é: {menor_caminho[target_node]}.')
    print(' -> '.join(reversed(caminho)))


# Definir o Grafo e chamar as funções:
'''nodes = ["Reykjavik", "Oslo", "Moscow", "London", "Rome", "Berlin", "Belgrade", "Athens"]

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
print_resultado(nodes_anteriores, menor_caminho, node_inicial, target_node) '''

# Obter dados do banco de dados
rows = fetch_data_from_db()
# Construir o grafo a partir dos dados do banco de dados
grafo = build_grafo_from_db_data(rows)

# Definir os nós inicial e alvo
node_inicial = 0 
target_node = 9 

nodes_anteriores, menor_caminho = dijkstra_algorithm(grafo, node_inicial)
print_resultado(nodes_anteriores, menor_caminho, node_inicial, target_node)