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
    
    # demilitando somente as variáveis
    df_cvli = df_ocorrencias[['aisp', 'cvli']]

    # Totalizar
    df_total_cvli = df_cvli.groupby(['aisp']).sum(['cvli']).reset_index()

    print(df_total_cvli.head())

    print('Dados obtidos com sucesso!')

except Exception as e:
    print(f'Erro ao obter dados: {e}')
    exit()

# obtendo medidas que suportarão as análises
try:
    print('Calculando medidas...')

    array_cvli = np.array(df_total_cvli['cvli'])

    # as medidas de tendência central
    media = np.mean(array_cvli)
    mediana = np.median(array_cvli)
    distancia_media_mediana = (media-mediana)/mediana

    print('\nMedidas de Tendência Central')
    print(30*'-')
    print(f'Média: {media}')
    print(f'Mediana: {mediana}')
    print(f'Dist. média x mediana: {distancia_media_mediana}')

    # medidas de posição e dispersão
    minimo = np.min(array_cvli)
    maximo = np.max(array_cvli)
    amplitude_total = maximo - minimo

    q1 = np.quantile(array_cvli, 0.25, method='weibull')
    q3 = np.quantile(array_cvli, 0.75, method='weibull')
    iqr = q3 - q1
    limite_inferior = q1 - (1.5*iqr)
    limite_superior = q3 + (1.5*iqr)

    print('\nMedidas de Posição e Dispersão')
    print(30*'-')
    print(f'Mínimo: {minimo}')
    print(f'Limite inferior: {limite_inferior}')
    print(f'Q1: {q1}')
    print(f'Q3: {q3}')
    print(f'IQR: {iqr}')
    print(f'Limite superior: {limite_superior}')
    print(f'Máximo: {maximo}')
    print(f'Amplitude total: {amplitude_total}')

    # identificar os outliers superiores
    df_outliers_max = df_total_cvli[df_total_cvli['cvli'] > limite_superior]

    print('\nAISPs com CVLIs superiores as demais:')
    print(30*'-')
    if len(df_outliers_max) == 0:
        print('Nenhum outlier encontrado.')
    else:
        print(df_outliers_max.sort_values(by='cvli', ascending=False))

except Exception as e:
    print(f'Erro ao calcular as medidas: {e}')
    exit()

# visualizando dados
try: 
    print('Visualizando dados...')
 
    plt.subplots(1,3,figsize=(15,5))

    plt.suptitle('Análise de CVLIs por AISPs', fontsize=18)

    # posição 1: boxplot do array_cvli
    plt.subplot(1,3,1)
    plt.boxplot(array_cvli,showmeans=True)
    plt.title('Boxplot de CVLIs por AISPs')
    plt.xlabel('CVLIs')
    plt.ylabel('Qtde CVLIs')

    # posição 2: Medidas
    plt.subplot(1,3,2)

    plt.text(0.1,0.9,f'Mínimo: {minimo}',fontsize=12)
    plt.text(0.1,0.8,f'Limite inferior: {limite_inferior}',fontsize=12)
    plt.text(0.1,0.7,f'Q1: {q1}',fontsize=12)
    plt.text(0.1,0.6,f'Mediana(Q2): {mediana}',fontsize=12)
    plt.text(0.1,0.5,f'Média: {media}',fontsize=12)
    plt.text(0.1,0.4,f'Dist. média x mediana: {distancia_media_mediana}',fontsize=12)
    plt.text(0.1,0.3,f'Q3: {q3}',fontsize=12)
    plt.text(0.1,0.2,f'Limite superior: {limite_superior}',fontsize=12)
    plt.text(0.1,0.1,f'Máximo: {maximo}',fontsize=12)
    plt.text(0.1,0.0,f'Amplitude total: {amplitude_total}',fontsize=12)

    plt.axis('off')

    #posição 3: Gráfico dos outliers
    plt.subplot(1,3,3)

    print(df_outliers_max.dtypes)
    df_outliers_max['aisp'] = df_outliers_max['aisp'].astype(str)
    print(df_outliers_max.dtypes)

    plt.bar(df_outliers_max['aisp'],df_outliers_max['cvli'])
    plt.title('Outliers de CVLIs por AISPs')
    plt.xlabel('BPMs')
    plt.ylabel('Qtde CVLIs')

    plt.tight_layout()
    plt.show()

except Exception as e:
    print(f'Erro ao visualizar dados: {e}')
    exit()