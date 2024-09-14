import pandas as pd
import numpy as np


# obter dados
try:
    print('Obtendo dados...')

    ENDERECO_DADOS = 'https://www.ispdados.rj.gov.br/Arquivos/BaseDPEvolucaoMensalCisp.csv'
    
    # encodings principais: https://docs.python.org/3/library/codecs.html#standard-encodings
    # utf-8, iso-8859-1, latin1, cp1252
    df_ocorrencias = pd.read_csv(ENDERECO_DADOS, sep=';', encoding='iso-8859-1')
    
    # demilitando somente as variáveis
    df_recup_veiculo = df_ocorrencias[['cisp', 'recuperacao_veiculos']]

    # Totalizar
    df_recup_veiculo = df_recup_veiculo.groupby(['cisp']).sum(['recuperacao_veiculos']).reset_index()

    print(df_recup_veiculo.head())

    print('Dados obtidos com sucesso!')

except Exception as e:
    print(f'Erro ao obter dados: {e}')
    exit()

# descrever a distribuição dos dados
try:
    print('Descrevendo a distribuição dos dados...')

    # Converter para um array numpy
    array_recup_veiculo = np.array(df_recup_veiculo['recuperacao_veiculos'])

    # medidas de tendência central
    media = np.mean(array_recup_veiculo)
    mediana = np.median(array_recup_veiculo)
    distancia_media_mediana = (media-mediana)/mediana

    # medidas de posição e dipersão
    q1 = np.quantile(array_recup_veiculo, 0.25, method='weibull')
    q3 = np.quantile(array_recup_veiculo, 0.75, method='weibull')
    iqr = q3 - q1
    minimo = np.min(array_recup_veiculo)
    limite_inferior = q1 - (1.5*iqr)
    limite_superior = q3 + (1.5*iqr)
    maximo = np.max(array_recup_veiculo)
    amplitute_total = maximo - minimo

    print('\nMedidas de Tendência Central')
    print(30*'-')
    print(f'Média: {media}')
    print(f'Mediana: {mediana}')
    print(f'Distância média da mediana: {distancia_media_mediana:.2f}')

    print('\nMedidas de Posição e Dispersão')
    print(30*'-')
    print(f'Menor valor: {minimo}')
    print(f'Limite inferior: {limite_inferior}')
    print(f'Q1: {q1}')
    print(f'Q3: {q3}')
    print(f'Limite superior: {limite_superior}')
    print(f'Maior valor: {maximo}')
    print(f'IQR: {iqr}')
    print(f'Amplitude total: {amplitute_total}')

    # listar as DPs coutliers superiores
    df_recup_veiculo_outliers_sup = df_recup_veiculo[df_recup_veiculo['recuperacao_veiculos'] > limite_superior]

    print('\nDPs com recuperações superiores as demais:')
    print(30*'-')
    if len(df_recup_veiculo_outliers_sup) == 0:
        print('Não existem DPs com valores discrepantes supreiores')
    else:
        print(df_recup_veiculo_outliers_sup.sort_values(by='recuperacao_veiculos', ascending=False))

    # listar as DPs coutliers inferiores
    df_recup_veiculo_outliers_inf = df_recup_veiculo[df_recup_veiculo['recuperacao_veiculos'] < limite_inferior]

    print('\nDPs com recuperações inferiores as demais:')
    print(30*'-')
    if len(df_recup_veiculo_outliers_inf) == 0:
        print('Não existem DPs com valores discrepantes inferiores')
    else:
        print(df_recup_veiculo_outliers_inf.sort_values(by='recuperacao_veiculos', ascending=True))

    # listar as DPS que menos recuperaram veículos
    df_recup_veiculo_q1 = df_recup_veiculo[df_recup_veiculo['recuperacao_veiculos'] < q1]

    print('\nDPs que menos recuperaram veículos:')
    print(30*'-')
    print(df_recup_veiculo_q1.sort_values(by='recuperacao_veiculos', ascending=True))

except Exception as e:
    print(f'Erro ao descrever os dados: {e}')
    exit()
