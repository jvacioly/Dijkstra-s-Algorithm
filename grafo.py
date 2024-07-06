class Grafo(object):
    def __init__(self, nodes, init_grafo):
        self.nodes = nodes
        self.grafo = self.construir_grafo(nodes, init_grafo)
    
    def construir_grafo(self, nodes, init_grafo):
        grafo = {}
        for node in nodes:
            grafo[node] = {}
        grafo.update(init_grafo)

        for node, edges in grafo.items():
            for node_adjacente, value in edges.items():
                if grafo[node_adjacente].get(node, False) == False:
                    grafo[node_adjacente][node] = value

        return grafo
    
    def get_nodes(self):
        return self.nodes
    
    def get_outgoing_edges(self, node):
        # Retorna os vizinhos do node
        connections = []
        for out_node in self.nodes:
            if self.grafo[node].get(out_node, False) != False:
                connections.append(out_node)
        return connections
    
    def value(self, node1, node2):
        return self.grafo[node1][node2]