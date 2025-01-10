import psycopg2
import csv

# Estabelecer a conexão com o banco de dados PostgreSQL
conexao = psycopg2.connect(
    host="localhost",
    dbname="postgres",
    user="postgres",
    password="", # senha do banco de dados que vc criar
    port=5432
)

# Criar um cursor para interagir com o banco de dados
cur = conexao.cursor()

# Abrir o arquivo CSV
with open('base_de_dados_csv/idh.csv', 'r') as file:
    # Criar um leitor de CSV
    leitor_csv = csv.reader(file)

    # Iterar sobre as linhas do CSV
    for linha in leitor_csv:
        nome = linha[0]  # País
        id = linha[1] #id
        ano = linha[2]
        idh = linha[3] 

        # Inserir dados na tabela pais
        cur.execute("""
            INSERT INTO idh (nome, id, ano, idh) 
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (id, ano) DO NOTHING;
        """, (nome, id, ano, idh))

# Confirmar as alterações no banco de dados
conexao.commit()

# Fechar o cursor e a conexão
cur.close()
conexao.close()
