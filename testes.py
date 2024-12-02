import datetime as dt
import pandas as pd

'''def fatura_proxima(df):

    df = df.copy()

    # Obter a data atual
    data_atual = dt.datetime.today().date()

    # Definir a data de início (dia 2 do mês atual)
    data_inicial = data_atual.replace(day=2, month=data_atual.month + 1)
    
    # Definir a data final (dia 2 do mês seguinte)
    if data_atual.month == 12:
        data_final = data_inicial.replace(year=data_atual.year + 1, month=1, day=2)
    elif data_atual.month == 11:
        data_final = data_inicial.replace(year=data_atual.year + 1, month=1, day=2)
    else:
        data_final = data_inicial.replace(month=data_inicial.month + 1, day=2)

    # Filtrar os dados entre as datas
    df_filtrado = df[(df['data'] >= data_inicial) & (df['data'] < data_final)]
    
    # Calcular a soma da coluna 'valor'
    soma_valores = df_filtrado['valor'].sum()
    return soma_valores

dataframe = pd.DataFrame({'data': ['2021-01-01', '2021-01-02', '2021-02-01', '2021-02-02']})

print(fatura_proxima(dataframe))'''

# dict_fatura = {'data': ['2021-01-01', '2021-02-02', '2021-03-01', '2021-04-02'], 'valor': [10, 20, 30, 40]}
# df_fatura = pd.DataFrame(dict_fatura)

# dict_proventos = {'data': ['2021-05-01', '2021-06-02', '2021-07-01', '2021-08-02'], 'valor': [5, 10, 15, 20]}
# df_proventos = pd.DataFrame(dict_proventos)

# def soma_valores_proventos_por_mes(df_fatura, df_proventos):

#     df_fatura = df_fatura.copy()
#     df_proventos = df_proventos.copy()

#     df_fatura['data'] = pd.to_datetime(df_fatura['data'])
#     df_proventos['data'] = pd.to_datetime(df_proventos['data'])

#     df = pd.merge(df_fatura, df_proventos, on='data', how='outer')
#     #df = pd.concat([df_fatura, df_proventos], axis=1, ignore_index=True)
#     #df = df_fatura.join(df_proventos, lsuffix='_fatura', rsuffix='_proventos')

#     # Group the data by month and year
#     df['mes'] = pd.to_datetime(df['data']).dt.to_period('M')
#     df_grouped = df.groupby('mes')['valor_x'].sum()

#     return df_grouped
#     #return df

# print(soma_valores_proventos_por_mes(df_fatura, df_proventos))

def fatura_proxima():

    #df = df.copy()

    # Obter a data atual
    data_atual = dt.datetime.today().date()

    # Definir a data de início (dia 2 do mês atual)
    if data_atual.month == 12:
        data_inicial = data_atual.replace(year=data_atual.year + 1, month=1, day=2)
    else:
        data_inicial = data_atual.replace(day=2, month=data_atual.month + 1)
    
    # Definir a data final (dia 2 do mês seguinte)
    if data_atual.month == 12:
        data_final = data_inicial.replace(month= data_inicial.month + 1, day=2)
    elif data_atual.month == 11:
        data_final = data_inicial.replace(year=data_atual.year + 1, month=1, day=2)
    else:
        data_final = data_inicial.replace(month=data_inicial.month + 1, day=2)

    '''    # Filtrar os dados entre as datas
        df_filtrado = df[(df['data'] >= data_inicial) & (df['data'] < data_final)]
        
        # Calcular a soma da coluna 'valor'
        soma_valores = df_filtrado['valor'].sum()
        return soma_valores'''

    print(data_inicial)
    print(data_final)

fatura_proxima()