import pandas as pd
import numpy as np

# obter dados
try:
    print('Obtendo dados...')

    ENDERECO_DADOS = 'https://www.ispdados.rj.gov.br/Arquivos/BaseDPEvolucaoMensalCisp.csv'
    
    # encodings principais: https://docs.python.org/3/library/codecs.html#standard-encodings
    # utf-8, iso-8859-1, latin1, cp1252
    df_ocorrencias = pd.read_csv(ENDERECO_DADOS, sep=';', encoding='iso-8859-1')
    
    # demilitando somente as variáveis do Exemplo01: munic e roubo_veiculo
    df_estelionato = df_ocorrencias[['mes_ano', 'estelionato']]

    # Totalizar roubo_veiculo por munic
    df_estelionato = df_estelionato.groupby(['mes_ano']).sum(['estelionato']).reset_index()

    #print(df_estelionato.head())

    print('Dados obtidos com sucesso!')

except Exception as e:
    print(f'Erro ao obter dados: {e}')
    exit()

# obter quartis
try:
    print('Otendo quartis....')

    array_estelionato = np.array(df_estelionato['estelionato'])

    # media e mediana
    media = np.mean(array_estelionato)
    mediana = np.median(array_estelionato)

    # distância entre media e mediana
    # até 10% a gente considera que a distribuição tende a uma simetria
    # Entre 10% e 25%, considera que a distribuição tende uma assimentria moderada, simetria moderada
    distancia = abs((media-mediana)/mediana)

    print('\nMedidas de tendência central: ')
    print(30*'-')
    print('Média: ', media)
    print('Mediana: ', mediana)
    print('Distância: ', distancia)

    # quartis
    q1 = np.quantile(array_estelionato, 0.25, method='weibull')
    q2 = np.quantile(array_estelionato, 0.50, method='weibull')
    q3 = np.quantile(array_estelionato, 0.75, method='weibull')

    print('\nMedidas de posição: ')
    print(30*'-')
    print('Q1 (25%): ',q1)
    print('Q2 (50%): ',q2)
    print('Q3 (75%): ',q3)

    print('\nMaiores meses e anos:')
    print(30*'-')
    df_mes_ano_acima_q3 = df_estelionato[df_estelionato['estelionato'] > q3]
    print(df_mes_ano_acima_q3.sort_values(by='estelionato',ascending=False))

    print('\nMenores meses e anos:')
    print(30*'-')
    df_mes_ano_abaixo_q1 = df_estelionato[df_estelionato['estelionato'] < q1]
    print(df_mes_ano_abaixo_q1.sort_values(by='estelionato'))
except Exception as e:
    print(f'Erro ao obter maiores e menores: {e}')
    exit()