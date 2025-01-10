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
with open('base_de_dados_csv/produtividade.csv', 'r') as file:
    # Criar um leitor de CSV
    leitor_csv = csv.reader(file)

    # Iterar sobre as linhas do CSV
    for linha in leitor_csv:
        id_pais = linha[0]  # País
        ano = linha[1]  # Código do país (ID)
        produtividade = linha[2]

        # Inserir dados na tabela pais
        cur.execute("""
            INSERT INTO produtividade (id, ano, produtividade)
            VALUES (%s, %s, %s)
            ON CONFLICT (id, ano) DO UPDATE SET produtividade = EXCLUDED.produtividade;
        """, (id_pais, int(ano), float(produtividade)))

# Confirmar as alterações no banco de dados
conexao.commit()

# Fechar o cursor e a conexão
cur.close()
conexao.close()
