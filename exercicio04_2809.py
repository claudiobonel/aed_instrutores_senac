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

    # filtrar os anos
    # \ significa que haverá uma quebra de linha
    df_ocorrencias = df_ocorrencias[(df_ocorrencias['ano'] >= 2022) \
                                    & (df_ocorrencias['ano'] <= 2023)]
    
    # demilitando somente as variáveis
    df_hom_doloso = df_ocorrencias[['aisp', 'hom_doloso']]

    # Totalizar
    df_total_hom_doloso = df_hom_doloso.groupby(['aisp']).sum(['hom_doloso']).reset_index()

    print(df_total_hom_doloso.head())

    print('Dados obtidos com sucesso!')

except Exception as e:
    print(f'Erro ao obter dados: {e}')
    exit()

# obtendo medidas que suportarão as análises
try:
    print('Obtendo medidas...')

    # assimetria
    assimentria = df_total_hom_doloso['hom_doloso'].skew()

    #curtose
    curtose = df_total_hom_doloso['hom_doloso'].kurtosis()

    # array de homicídios dolosos
    array_hom_doloso = np.array(df_total_hom_doloso['hom_doloso'])

    #medidas de tendência central
    media = np.mean(array_hom_doloso)
    mediana = np.median(array_hom_doloso)
    distancia_media_mediana = (media-mediana)/mediana

    #medidas de dispersao
    variancia = np.var(array_hom_doloso)
    distancia_media_variancia = variancia/(media**2)
    desvio_padrao = np.std(array_hom_doloso)
    # é a mesma coisa que utilizar o método std
    #desvio_padrao = np.sqrt(variancia)
    coeficiente_variacao = desvio_padrao/media
    minimo = np.min(array_hom_doloso)
    maximo = np.max(array_hom_doloso)
    amplitude_total = maximo - minimo

    # medidas de posição
    q1 = np.quantile(array_hom_doloso, 0.25, method='weibull')
    q3 = np.quantile(array_hom_doloso, 0.75, method='weibull')
    iqr = q3 - q1
    limite_superior = q3 + (1.5*iqr)

    print('\nMedidas de assimetria e curtose:')
    print(30*'-')
    print(f'Assimetria: {assimentria}')
    print(f'Curtose: {curtose}')

    print('\nMedidas de tendência central:')
    print(30*'-')
    print(f'Média: {media}')
    print(f'Mediana: {mediana}')
    print(f'Distância média x mediana: {distancia_media_mediana}')

    print('\nMedidas de dispersão:')
    print(30*'-')
    print(f'Variância: {variancia}')
    print(f'Distância média x variância: {distancia_media_variancia}')
    print(f'Desvio padrão: {desvio_padrao}')
    print(f'Coeficiente de variação: {coeficiente_variacao}')
    print(f'Amplitude total: {amplitude_total}')

    print('\nMedidas de posição:')
    print(30*'-')
    print(f'Menor valor: {minimo}')
    print(f'Q1: {q1}')
    print(f'Q3: {q3}')
    print(f'IQR: {iqr}')
    print(f'Limite superior: {limite_superior}')
    print(f'Maior valor: {maximo}')

    # identificar os outliers superiores
    df_hom_doloso_outliers = df_total_hom_doloso[df_total_hom_doloso['hom_doloso'] > limite_superior]

    # visualizando os outliers
    print('\nAISPs com homicídios dolosos superiores as demais:')
    print(30*'-')
    if len(df_hom_doloso_outliers) == 0:
        print('Nenhum outlier encontrado.')
        df_total_hom_doloso_final = df_total_hom_doloso.copy()
    else:
        df_total_hom_doloso_final = df_hom_doloso_outliers.copy()
        
    print(df_total_hom_doloso_final.sort_values(by='hom_doloso', ascending=False))

except Exception as e:
    print(f'Erro ao obter medidas: {e}')
    exit()

# exbir em um painel
try: 
    print('Visualizando dados...')

    plt.subplots(1,3,figsize=(16,6))
    plt.suptitle('Análise de Homicídios Dolosos por AISP', fontsize=18)

    #posição 1: Ranking de homicídios dolosos
    plt.subplot(1,3,1)

    # converter ainsp par string
    df_total_hom_doloso_final['aisp'] = df_total_hom_doloso_final['aisp'].astype(str)

    # ordenar o dataframe
    df_total_hom_doloso_final = df_total_hom_doloso_final.sort_values(by='hom_doloso', ascending=True)

    # plotar o gráfico
    plt.barh(df_total_hom_doloso_final['aisp'], df_total_hom_doloso_final['hom_doloso'])
    plt.xlabel('Homicídios Dolosos')
    plt.ylabel('BPMs')
    plt.title('Homicídios Dolosos por AISP')

    # posição 2: histograma
    plt.subplot(1,3,2)
    plt.hist(array_hom_doloso, bins=100, color='blue', edgecolor='black')

    plt.axvline(media, color='red',linewidth=1)

    plt.title('Histograma de Homicídios Dolosos por AISP')

    #posição 3: medidas
    plt.subplot(1,3,3)

    plt.text(0.1,1.0,f'Assimetria: {assimentria}',fontsize=12)
    plt.text(0.1,0.9,f'Curtose: {curtose}',fontsize=12)
    plt.text(0.1,0.8,f'Média: {media}',fontsize=12)
    plt.text(0.1,0.7,f'Mediana(Q2): {mediana}',fontsize=12)
    plt.text(0.1,0.6,f'Dist. média x mediana: {distancia_media_mediana}',fontsize=12)
    plt.text(0.1,0.5,f'Variância: {variancia}',fontsize=12)
    plt.text(0.1,0.4,f'Dist. média x variância: {distancia_media_variancia}',fontsize=12)
    plt.text(0.1,0.3,f'Desvio padrão: {desvio_padrao}',fontsize=12)
    plt.text(0.1,0.2,f'Coeficiente de variação: {coeficiente_variacao}',fontsize=12)
    plt.text(0.1,0.1,f'Amplitude total: {amplitude_total}',fontsize=12)

    plt.axis('off')

    plt.tight_layout()
    plt.show()

except Exception as e:
    print(f'Erro ao visualizar dados: {e}')
    exit()