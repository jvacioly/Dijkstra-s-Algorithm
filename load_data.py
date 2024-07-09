import psycopg2

def create_or_alter_graph_table():
    # Parâmetros de conexão ao banco de dados
    db_name = 'postgres'
    db_user = 'postgres'
    db_password = '1234'
    db_host = 'localhost' 
    db_port = '5432'  

    # Conectando ao banco de dados
    try:
        connection = psycopg2.connect(
            dbname=db_name,
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port
        )
        cursor = connection.cursor()
        
        # Verificação se a tabela já existe
        check_table_query = '''
        SELECT EXISTS (
            SELECT FROM information_schema.tables 
            WHERE table_name = 'grafo'
        );
        '''
        cursor.execute(check_table_query)
        table_exists = cursor.fetchone()[0]

        if table_exists:
            print("A tabela já existe. Alterando a tabela se necessário.")
            alter_table_query = '''
            DO $$
            BEGIN
                IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='grafo' AND column_name='vertice1') THEN
                    ALTER TABLE grafo ADD COLUMN vertice1 INT NOT NULL;
                END IF;
                IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='grafo' AND column_name='vertice2') THEN
                    ALTER TABLE grafo ADD COLUMN vertice2 INT NOT NULL;
                END IF;
                IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='grafo' AND column_name='peso') THEN
                    ALTER TABLE grafo ADD COLUMN peso FLOAT NOT NULL;
                END IF;
            END $$;
            '''
            cursor.execute(alter_table_query)
            connection.commit()
        else:
            print("A tabela não existe. Criando a tabela.")
            create_table_query = '''
            CREATE TABLE grafo (
                vertice1 INT NOT NULL,
                vertice2 INT NOT NULL,
                peso FLOAT NOT NULL
            );
            '''
            cursor.execute(create_table_query)
            connection.commit()
            print("Tabela criada com sucesso")
        
        # Remover todos os dados da tabela antes de inserir novos dados
        cursor.execute('DELETE FROM grafo')
        connection.commit()
        print("Todos os dados existentes foram removidos.")
        
        # Inserção dos dados do arquivo na tabela
        insert_data_from_file(cursor, connection, 'dados\\bio-CE-GT\\bio-CE-GT.edges') # CAMINHO DO ARQUIVO
        
    except (Exception, psycopg2.Error) as error:
        print("Erro ao conectar ou modificar a tabela no PostgreSQL", error)
        
    finally:
        # Fechando a conexão com o banco de dados
        if connection:
            cursor.close()
            connection.close()
            print("Conexão com o PostgreSQL fechada")

def insert_data_from_file(cursor, connection, file_path):
    try:
        with open(file_path, 'r') as file:
            for line in file:
                vertice1, vertice2, peso = map(float, line.split())

                insert_query = '''
                INSERT INTO grafo (vertice1, vertice2, peso)
                VALUES (%s, %s, %s);
                '''
                cursor.execute(insert_query, (int(vertice1), int(vertice2), peso))
        connection.commit()
        print("Dados inseridos com sucesso")
    except (Exception, psycopg2.Error) as error:
        print("Erro ao ler o arquivo ou inserir dados no PostgreSQL", error)

# Chamada da função para criar ou alterar a tabela
create_or_alter_graph_table()
