import psycopg2

conexao = psycopg2.connect(
    host = "localhost",
    dbname = "postgres",
    user = "postgres",
    password="", # senha do banco de dados que vc criar
    port = 5432
);

cur = conexao.cursor();

cur.execute("""
""");

conexao.commit();

cur.close();
conexao.close();