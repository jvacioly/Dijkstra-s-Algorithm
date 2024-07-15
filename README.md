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

## Como o Código Funciona?
- Configuração do Ambiente
> Utilizamos o Docker para hospedar o banco de dados PostgreSQL, o que facilita a implantação e a manutenção do sistema. Para visualizar e gerenciar o banco de dados, utilizamos a ferramenta DBeaver, que nos fornece uma interface amigável e poderosa.
- Estrutura de Dados
- Análise do Grafo
  - Algoritmo de Busca
  - Representação Visual
  
###### Dijkstra's Algorithm, projeto da disciplina de Algoritmos e Estruturas de Dados 2024.1 CIn/UFPE
