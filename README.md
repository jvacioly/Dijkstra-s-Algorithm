# Dijkstra-s-Algorithm
Este é um projeto da disciplina de Algoritmos e Estruturas de Dados 2024.1. O foco do projeto é construir um programa que crie e analise um grafo utilizando dados de um banco de dados PostgresSQL. A análise do grafo consiste em encontrar a melhor rota entre dois nós através do algoritmo de Dijkstra.

## Itens Necessários
- WSL <https://medium.com/@habbema/desvendando-o-wsl-2-no-windows-11-c7649545026d>
- Docker <https://www.docker.com/products/docker-desktop/>
- DBeaver <https://dbeaver.io/download/>

## Como Rodar
Após baixar todos os itens necessários, no Docker crie um container com a imagem do Postgres e dê run nesse container.
No DBeaver, conecte com o banco de dados que você acabou de criar. Em seguida, dentro do DBeaver, crie um script com o seguinte código:
~~~sql
select * from grafo g 
~~~
No VScode, rode o script load_data para carregar os dados na tabela do banco de dados. De volta ao DBeaver rode o script que criamos para visualizar a tabela.
Agora já é possível rodar o código principal do dijkstra.

## Bibliotecas Utilizadas
- sys
> Utilizado para acessar parâmetros e funções específicas do sistema.
- psycopg2
> Uma biblioteca Python que permite conectar e executar operações no banco de dados PostgreSQL.
- networkx
> Biblioteca para a criação, manipulação e estudo da estrutura e dinâmica de grafos complexos.
- matplotlib
> Utilizamos os módulos pyplot e animation. O primeiro serve para a criação de gráficos e visualizações, enquanto o segundo cria animações.

## Como o Código Funciona?
- Configuração do Ambiente
> Utilizamos o Docker para hospedar o banco de dados PostgreSQL, o que facilita a implantação e a manutenção do sistema. Para visualizar e gerenciar o banco de dados, utilizamos a ferramenta DBeaver, que nos fornece uma interface amigável e poderosa.
- Carregar Dados
> O sript load_data.py se conecta ao banco de dados PostgreSQL, verifica a existência de uma tabela de grafo, cria ou altera a tabela conforme necessário, remove todos os dados existentes e, em seguida, insere novos dados de um arquivo.
- Estrutura de Dados
>  Através do scrip grafo.py cria uma classe Grafo que modela um grafo com nós e arestas. A classe possui métodos para construir o grafo, retornar os nós, obter os vizinhos de um nó e o peso das conexões entre dois nós. A utilização de dicionários facilita a estruturação e a manipulação dos dados do grafo. Através dessa implementação, podemos realizar análises de grafos, como encontrar caminhos e distâncias entre diferentes nós, de maneira eficiente.
- Análise do Grafo
  - Algoritmo de Busca
  > Utilizando o algoritmo de Dijkstra, a função dijkstra_algorithm encontra o menor caminho entre dois nós no grafo. Depois de percorrer todo o grafo ela retorna a distância do caminho mais eficiênte e uma lista dos nós desse caminho.
  - Representação Visual
  > Utiliza a biblioteca NetworkX e Matplotlib para desenhar o grafo. Anima a visualização do algoritmo de Dijkstra, mostrando os nós visitados e o caminho mais curto.
  
###### Dijkstra's Algorithm, projeto da disciplina de Algoritmos e Estruturas de Dados 2024.1 CIn/UFPE
