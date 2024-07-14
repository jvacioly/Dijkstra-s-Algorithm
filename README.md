# Dijkstra-s-Algorithm
Dijkstra's Algorithm, projeto da disciplina de Algoritmos e Estruturas de Dados 2024.1

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

## Como o Código Funciona?
- grafo.py
- load_data.py
- dijkstra.py
  - Algoritmo de Busca
  - Representação Visual
  
