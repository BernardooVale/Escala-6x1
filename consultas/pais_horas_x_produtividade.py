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
           prod.produtividade
    FROM pais p
    JOIN horas_trabalhadas ht ON p.id = ht.id
    JOIN produtividade prod ON p.id = prod.id AND ht.ano = prod.ano
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

def criar_grafico(dados, pais_id, arquivo_imagem='grafico.png'):
    anos, horas, produtividade = zip(*dados)
    
    # Criar gráfico de dispersão
    plt.figure(figsize=(10, 6))
    plt.scatter(produtividade, horas, color='blue', label='Pontos (Ano)', zorder=3)
    
    # Adicionar rótulos aos pontos
    for i, ano in enumerate(anos):
        plt.text(produtividade[i], horas[i], str(ano), fontsize=9, ha='right')

    # Ajustar curva de tendência (polinômio de grau 2 - curva quadrática)
    coef = np.polyfit(produtividade, horas, 2)  # Ajuste quadrático
    tendencia = np.poly1d(coef)
    x_vals = np.linspace(min(produtividade), max(produtividade), 100)  # Gerar valores x para a linha curva
    plt.plot(x_vals, tendencia(x_vals), color='red', linestyle='-', label='Curva de Tendência', zorder=2)

    # Configurar o gráfico
    plt.title(f'Relação entre Produtividade e Horas Trabalhadas ({pais_id})')
    plt.xlabel('Produtividade')
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
    arquivo_imagem = f'{pais_id}_produtividade_horas.png'
    criar_grafico(dados, pais_id, arquivo_imagem)
    print(f"Gráfico salvo como {arquivo_imagem}")
else:
    print(f"Nenhum dado encontrado para o país {pais_id}.")

# Fechar a conexão
conexao.close()
