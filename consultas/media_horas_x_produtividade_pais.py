import psycopg2
import matplotlib.pyplot as plt
import numpy as np

def conectar_banco():
    try:
        conexao = psycopg2.connect(
            host="localhost",
            dbname="postgres",
            user="postgres",
            password="",  # senha do banco de dados que vc criar
            port=5432
        )
        return conexao
    except psycopg2.OperationalError as e:
        print(f"Erro ao conectar ao banco: {e}")
        raise

def obter_dados(conexao):
    consulta = """
    SELECT p.nome,
           AVG(ht.horas) AS media_horas_trabalhadas,
           AVG(prod.produtividade) AS media_produtividade
    FROM pais p
    JOIN horas_trabalhadas ht ON p.id = ht.id
    JOIN produtividade prod ON p.id = prod.id AND ht.ano = prod.ano
    GROUP BY p.nome;
    """
    try:
        with conexao.cursor() as cur:
            cur.execute(consulta)
            resultados = cur.fetchall()
        return resultados
    except Exception as e:
        print(f"Erro ao executar a consulta: {e}")
        raise

def criar_grafico(dados, arquivo_imagem='grafico.png'):
    nomes, medias_horas, medias_produtividade = zip(*dados)
    
    # Criar gráfico de dispersão
    plt.figure(figsize=(10, 6))
    plt.scatter(medias_produtividade, medias_horas, color='blue', label='Pontos (País)', zorder=3)
    
    # Adicionar rótulos aos pontos
    for i, nome in enumerate(nomes):
        plt.text(medias_produtividade[i], medias_horas[i], nome, fontsize=9, ha='right')

    # Ajustar curva de tendência (polinômio de grau 2 - curva quadrática)
    coef = np.polyfit(medias_produtividade, medias_horas, 2)  # Ajuste quadrático
    tendencia = np.poly1d(coef)
    x_vals = np.linspace(min(medias_produtividade), max(medias_produtividade), 100)  # Gerar valores x para a linha curva
    plt.plot(x_vals, tendencia(x_vals), color='red', linestyle='-', label='Curva de Tendência', zorder=2)

    # Configurar o gráfico
    plt.title('Relação entre Produtividade e Horas Trabalhadas por País')
    plt.xlabel('Média de Produtividade')
    plt.ylabel('Média de Horas Trabalhadas')
    plt.grid(True, linestyle='--', alpha=0.7, zorder=1)
    plt.legend()
    plt.tight_layout()

    # Salvar o gráfico como uma imagem PNG
    plt.savefig(arquivo_imagem, format='png')

# Conectar ao banco e obter dados
conexao = conectar_banco()
dados = obter_dados(conexao)

if dados:
    # Nome do arquivo PNG onde o gráfico será salvo
    arquivo_imagem = 'grafico_produtividade_horas_por_pais.png'
    criar_grafico(dados, arquivo_imagem)
    print(f"Gráfico salvo como {arquivo_imagem}")
else:
    print("Nenhum dado encontrado para criar o gráfico.")

# Fechar a conexão
conexao.close()
