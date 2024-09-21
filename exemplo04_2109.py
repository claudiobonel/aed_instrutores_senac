import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# obter dados
try:
    print('Obtendo dados...')

    ENDERECO_DADOS = 'https://www.ispdados.rj.gov.br/Arquivos/BaseDPEvolucaoMensalCisp.csv'
    
    # encodings principais: https://docs.python.org/3/library/codecs.html#standard-encodings
    # utf-8, iso-8859-1, latin1, cp1252
    df_ocorrencias = pd.read_csv(ENDERECO_DADOS, sep=';', encoding='iso-8859-1')
    
    # demilitando somente as variáveis do Exemplo01: munic e roubo_veiculo
    df_roubo_veiculo = df_ocorrencias[['munic', 'roubo_veiculo']]

    # Totalizar roubo_veiculo por munic
    df_roubo_veiculo = df_roubo_veiculo.groupby(['munic']).sum(['roubo_veiculo']).reset_index()

    print(df_roubo_veiculo.head())

    print('Dados obtidos com sucesso!')

except Exception as e:
    print(f'Erro ao obter dados: {e}')
    exit()

# obter informações sobre padrão de roubo_veiculo
try:
    print('Obtendo informações sobre padrão de roubo de veículos...')

    # array é uma estrutura de dados que armazena uma coleção de dados
    # e computacionalmente é mais eficiente para calcular estatísticas
    # Faz parte da biblioteca numpy
    array_roubo_veiculo = np.array(df_roubo_veiculo['roubo_veiculo'])

    # média de roubo_veiculo
    media_roubo_veiculo = np.mean(array_roubo_veiculo)

    # mediana de roubo_veiculo
    # divide a distribuição em duas partes iguais (50% dos dados abaixo e 50% acima)
    mediana_roubo_veiculo = np.median(array_roubo_veiculo)

    # distânicia
    distancia = abs((media_roubo_veiculo-mediana_roubo_veiculo)/mediana_roubo_veiculo)

    # Medidas de tendência central
    # Se a média for muito diferente da mediana, distribuição é assimétrica. Não tende a haver um padrão
    # e pode ser que existam outliers (valores discrepantes)
    # Se a média for próxima (25%) a mediana, distribuição é simétrica. Tende a haver um padrão
    print('\nMedidas de tendência central: ')
    print(30*'-')
    print(f'Média de roubo de veículos: {media_roubo_veiculo}')
    print(f'Mediana de roubo de veículos: {mediana_roubo_veiculo}')
    print(f'Distância entre média e mediana: {distancia}')

    # Medidas de dispersão
    # Amplitude total
    # Maior valor - menor valor
    # Quanto mais próximo de zero, maior a homogeinidade dos dados
    # Se for igual a zero, todos os valores são iguais
    # Quanto masi próximo do máximo, maior a dispersão dos dados ou heterogeneidade
    maximo = np.max(array_roubo_veiculo)
    minimo = np.min(array_roubo_veiculo)
    amplitude = maximo - minimo

    print('\nMedidas de dispersão: ')
    print(30*'-')
    print('Máximo: ', maximo)
    print('Mínimo: ', minimo)
    print('Amplitude total: ', amplitude)

    # Quartis
    # Método padrão é o weibull 
    q1 = np.quantile(array_roubo_veiculo, 0.25, method='weibull') # Q1 é 25% 
    q2 = np.quantile(array_roubo_veiculo, 0.50, method='weibull') # Q2 é 50% (mediana)
    q3 = np.quantile(array_roubo_veiculo, 0.75, method='weibull') # Q3 é 75%

    # IQR (Intervalo interquartil)
    # q3 - q1
    # é a amplitude do intervalo dos 50% dos dados centrais
    # Ela ignora os valores extremos. Max e min estão fora do IQR
    # Não sofre a interferência dos valores extremos
    # quanto mais próximo de zero, mais homogêneo são os dados
    # quanto mais próximo do q3, mais heterogêneo são os dados
    iqr = q3 - q1

    # limite superior
    # vai identificar os outliers acima de q3
    limite_superior = q3 + (1.5 * iqr)

    # limite inferior
    # vai identificar os outliers abaixo de q1
    limite_inferior = q1 - (1.5 * iqr)

    # medidas de posição (ou de dispersão)
    print('\nMedidas de posição: ')
    print(30*'-')
    print('Mínimo: ', minimo)
    print(f'Limite inferior: {limite_inferior}')
    print(f'Q1: {q1}')
    print(f'Q2: {q2}')
    print(f'Q3: {q3}')
    print(f'IQR: {iqr}')
    print(f'Limite superior: {limite_superior}')
    print('Máximo: ', maximo)

    # filtrar o dataframe df_roubo_veiculo para o munics com roubo de veículo abaixo q1
    df_roubo_veiculo_outliers_inferiores = df_roubo_veiculo[df_roubo_veiculo['roubo_veiculo'] < limite_inferior]

    # filtrar o dataframe df_roubo_veiculo para o munics com roubo de veículo acima q3
    df_roubo_veiculo_outliers_superiores = df_roubo_veiculo[df_roubo_veiculo['roubo_veiculo'] > limite_superior]

    print('\nMunicípios com outliers inferiores: ')
    print(30*'-')
    if len(df_roubo_veiculo_outliers_inferiores) == 0:
        print('Não existem outliers inferiores!')
    else:
        print(df_roubo_veiculo_outliers_inferiores.sort_values(by='roubo_veiculo', ascending=True))


    print('\nMunicípios com outliers superiores: ')
    print(30*'-')
    if len(df_roubo_veiculo_outliers_superiores) == 0:
        print('Não existe outliers superiores!')
    else:
        print(df_roubo_veiculo_outliers_superiores.sort_values(by='roubo_veiculo', ascending=False))

except Exception as e:
    print(f'Erro ao obter informações sobre padrão de roubo de veículos: {e}')
    exit()


# Medidas de distribuição
try:
    print('Calculando medidas de distribuição...')

    # Assimentria. Skewness
    # é uma medida que descreverá o quanto uma distribuição é simétrica ou assimétrica
    # quanto mais próximo de 0 (-0.5 a 0.5) mais simétrica é a distribuição. Os dados estão distribuídos de forma homogênea
    # ao redor da média
    # Acima de 0.5, a assimetria é positiva, os dados estão mais concentrados na parte maior da distribuição.
    # os dados maiores estão puxando a média para cima. Tende a ser maior que a mediana
    # 0.5 a 1.0 é uma assimetria moderada. Assimetria acima 1.0 é uma assimetria alta
    # Abaixo de -0.5, a assimetria é negativa, os dados estão mais concentrados na parte menor da distribuição.
    # os dados menores estão puxando a média para baixo. Tende a ser menor que a mediana
    # -0.5 a -1.0 é uma assimetria moderada. Assimetria abaixo -1.0 é uma assimetria alta
    assimetria = df_roubo_veiculo['roubo_veiculo'].skew()

    #curtpse. Kurtosis
    curtose = df_roubo_veiculo['roubo_veiculo'].kurtosis()

    print('\nMedidas de distribuição: ')
    print(30*'-')
    print(f'Assimetria: {assimetria}')
    print(f'Curtose: {curtose}')

except Exception as e:
    print(f'Erro ao calcular as medidas de distribuição: {e}')
    exit()

# medidas de dispersão
try:
    print('Calculando medidas de dispersão...')

    # É uma medida para obsersar a dispersão dos dados
    # observa-se em relação a média
    # é a média dos quadrados das diferenças entre cada valor e a média
    # o resultado da variância é elevado ao quadrado
    variancia = np.var(array_roubo_veiculo)

    # distância da variância para a média
    distancia_var_media = variancia/(media_roubo_veiculo**2)

    # devio padrão é a raiz quadrada da variância
    # apresentar o quanto os dados estão afastados da média (para mais ou para menos). Valor absoluto
    desvio_padrao = np.std(array_roubo_veiculo)

    # coeficiente de variação
    # é a magnitude do desvio padrão em realção a média
    coef_variacao = desvio_padrao/media_roubo_veiculo

    print('\nMedidas de dispersão: ')
    print(30*'-')
    print(f'Variância: {variancia}')
    print(f'Dist. var x média: {distancia_var_media}')
    print(f'Desvio padrão: {desvio_padrao}')
    print(f'Coef. variação: {coef_variacao}')

except Exception as e:
    print(f'Erro ao calcular as medidas de dispersão: {e}')
    exit()

# visualizar os dados
try:
    print('Visualizando os dados...')

    # matplotlib é uma biblioteca para visualização de dados
    # site é https://matplotlib.org/
    # pip install matplotlib

    plt.subplots(2,2, figsize=(16,7))
    plt.suptitle('Análise de roubo de veículos no RJ')

    # posição 1: bloxplot sem outliers
    plt.subplot(2,2,1)
    plt.boxplot(array_roubo_veiculo, vert=False, showmeans=True, meanline=True)
    plt.title('Boxplot com outliers') 

    # posição 2: histograma de roubo de veículos
    plt.subplot(2,2,2)
    plt.hist(array_roubo_veiculo, bins=100, edgecolor='black')
    #plt.axvline(media_roubo_veiculo, color='r', linewidth=1)
    #plt.axvline(mediana_roubo_veiculo, color='g', linewidth=1)

    # posição 3: Ranking das cidades outliers superiores
    plt.subplot(2,2,3)

    # ordenar
    df_roubo_veiculo_outliers_superiores_ordered = df_roubo_veiculo_outliers_superiores.sort_values(by='roubo_veiculo', ascending=True)

    plt.barh(df_roubo_veiculo_outliers_superiores_ordered['munic'], df_roubo_veiculo_outliers_superiores_ordered['roubo_veiculo'])
    
    plt.title('Ranking dos municípios com outliers superiores')

    #posição 4: Medidas descritivas
    plt.subplot(2,2,4)

    plt.text(0.1, 0.9, f'Média: {media_roubo_veiculo}', fontsize=12)
    plt.text(0.1, 0.8, f'Mediana: {mediana_roubo_veiculo}', fontsize=12)
    plt.text(0.1, 0.7, f'Distância: {distancia}', fontsize=12)
    plt.text(0.1, 0.6,f'Menor valor: {minimo}', fontsize=12)
    plt.text(0.1, 0.5,f'Limite inferior: {limite_inferior}', fontsize=12)
    plt.text(0.1, 0.4,f'Q1: {q1}', fontsize=12)
    plt.text(0.1, 0.3,f'Q3: {q3}', fontsize=12)
    plt.text(0.1, 0.2,f'Limite superior: {limite_superior}', fontsize=12)
    plt.text(0.1, 0.1,f'Maior valor: {maximo}', fontsize=12)
    plt.text(0.1, 0.0,f'Amplitude Total: {amplitude}', fontsize=12)

    plt.text(0.7, 0.9, f'Assimetria: {assimetria}', fontsize=12)
    plt.text(0.7, 0.8, f'Curtose: {curtose}', fontsize=12)
    plt.text(0.7, 0.7, f'Variância: {variancia}', fontsize=12)
    plt.text(0.7, 0.6, f'Distância var x média: {distancia_var_media}', fontsize=12)
    plt.text(0.7, 0.5, f'Desvio padrão: {desvio_padrao}', fontsize=12)
    plt.text(0.7, 0.4, f'Coef. variação: {coef_variacao}', fontsize=12)

    # desativar os eixos
    plt.axis('off')

    # ajsutar o layout
    plt.tight_layout()

    # exibir o painel
    plt.show()
    
except Exception as e:
    print(f'Erro ao descrever os dados: {e}')
    exit()