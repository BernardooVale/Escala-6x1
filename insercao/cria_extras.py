import psycopg2

conexao = psycopg2.connect(
    host = "localhost",
    dbname = "postgres",
    user = "postgres",
    password="", # senha do banco de dados que vc criar
    port = 5432
);

cur = conexao.cursor();

cur.execute("""CREATE TABLE IF NOT EXISTS idh (
    nome VARCHAR(50),
    id CHAR(3),
    ano INT,
    idh FLOAT NOT NULL,
    PRIMARY KEY (id, ano)
);
""");

conexao.commit();

cur.close();
conexao.close();