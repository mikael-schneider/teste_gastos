import datetime as dt
import pandas as pd

def fatura_proxima(df):

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

print(fatura_proxima(dataframe))

