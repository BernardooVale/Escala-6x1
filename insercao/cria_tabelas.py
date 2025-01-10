import psycopg2

conexao = psycopg2.connect(
    host = "localhost",
    dbname = "postgres",
   user = "postgres",
    password="", # senha do banco de dados que vc criar
    port = 5432
);

cur = conexao.cursor();

cur.execute("""CREATE TABLE IF NOT EXISTS pais (
    id CHAR(3) PRIMARY KEY,
    nome VARCHAR(50) NOT NULL
);
""");

cur.execute("""CREATE TABLE IF NOT EXISTS horas_trabalhadas (
    ID CHAR(3),
    ano INT,
    horas FLOAT NOT NULL,
    PRIMARY KEY (ID, ano),
    FOREIGN KEY (ID) REFERENCES pais(ID) ON DELETE CASCADE ON UPDATE CASCADE
);
""");

cur.execute("""CREATE TABLE IF NOT EXISTS per_capita (
    ID CHAR(3),
    ano INT,
    PIB_per_capita FLOAT NOT NULL,
    PRIMARY KEY (ID, ano),
    FOREIGN KEY (ID) REFERENCES pais(ID) ON DELETE CASCADE ON UPDATE CASCADE
);
""");

cur.execute("""CREATE TABLE IF NOT EXISTS produtividade (
    ID CHAR(3),
    ano INT,
    produtividade FLOAT NOT NULL,
    PRIMARY KEY (ID, ano),
    FOREIGN KEY (ID) REFERENCES pais(ID) ON DELETE CASCADE ON UPDATE CASCADE
);
""");

conexao.commit();

cur.close();
conexao.close();