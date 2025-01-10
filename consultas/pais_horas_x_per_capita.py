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

def obter_dados(conexao, pais_id):
    consulta = """
    SELECT ht.ano,
           ht.horas,
           pc.PIB_per_capita
    FROM pais p
    JOIN horas_trabalhadas ht ON p.id = ht.id
    JOIN per_capita pc ON p.id = pc.id AND ht.ano = pc.ano
    WHERE p.id = %s;
    """
    try:
        with conexao.cursor() as cur:
            cur.execute(consulta, (pais_id,))
            resultados = cur.fetchall()
        return resultados
    except Exception as e:
        print(f"Erro ao executar a consulta: {e}")
        raise

def criar_grafico(dados, pais_id, arquivo_imagem='pais_horas_x_per_capita.png'):
    anos, horas, pib_per_capita = zip(*dados)
    
    # Criar gráfico de dispersão
    plt.figure(figsize=(10, 6))
    plt.scatter(pib_per_capita, horas, color='blue', label='Pontos (Ano)', zorder=3)
    
    # Adicionar rótulos aos pontos
    for i, ano in enumerate(anos):
        plt.text(pib_per_capita[i], horas[i], str(ano), fontsize=9, ha='right')

    # Ajustar curva de tendência (polinômio de grau 2 - curva quadrática)
    coef = np.polyfit(pib_per_capita, horas, 2)  # Ajuste quadrático
    tendencia = np.poly1d(coef)
    x_vals = np.linspace(min(pib_per_capita), max(pib_per_capita), 100)  # Gerar valores x para a linha curva
    plt.plot(x_vals, tendencia(x_vals), color='red', linestyle='-', label='Curva de Tendência', zorder=2)

    # Configurar o gráfico
    plt.title(f'Relação entre PIB per Capita e Horas Trabalhadas ({pais_id})')
    plt.xlabel('PIB per Capita')
    plt.ylabel('Horas Trabalhadas')
    plt.grid(True, linestyle='--', alpha=0.7, zorder=1)
    plt.legend()
    plt.tight_layout()

    # Salvar o gráfico como uma imagem PNG
    plt.savefig(arquivo_imagem, format='png')

# Defina a variável pais_id com o ID do país desejado (ex: 'BRA' para Brasil)
pais_id = 'BRA'

# Conectar ao banco e obter dados
conexao = conectar_banco()
dados = obter_dados(conexao, pais_id)

if dados:
    # Nome do arquivo PNG onde o gráfico será salvo
    arquivo_imagem = f'{pais_id}_per_capita_horas.png'
    criar_grafico(dados, pais_id, arquivo_imagem)
    print(f"Gráfico salvo como {arquivo_imagem}")
else:
    print(f"Nenhum dado encontrado para o país {pais_id}.")

# Fechar a conexão
conexao.close()