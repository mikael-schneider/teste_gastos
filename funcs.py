import datetime as dt
import pandas as pd

def formatar_valor_brasileiro(valor):
    valor_str = f"{valor:,.2f}"
    valor_str = valor_str.replace(",", "X").replace(".", ",").replace("X", ".")
    return valor_str

def ano_atual():

    return dt.datetime.today().year

def fatura_atual(df):

    df = df.copy()

    # Obter a data atual
    data_atual = dt.datetime.today().date()

    # Definir a data de início (dia 2 do mês atual)
    data_inicial = data_atual.replace(day=2)
    
    # Definir a data final (dia 2 do mês seguinte)
    if data_atual.month == 12:
        data_final = data_atual.replace(year=data_atual.year + 1, month=1, day=2)
    else:
        data_final = data_atual.replace(month=data_atual.month + 1, day=2)

    # Filtrar os dados entre as datas
    df_filtrado = df[(df['data'] >= data_inicial) & (df['data'] < data_final)]

    # Calcular a soma da coluna 'valor'
    soma_valores = df_filtrado['valor'].sum()
    
    return soma_valores

def fatura_anterior(df):

    df = df.copy()

    # Obter a data atual
    data_atual = dt.datetime.today().date()

    # Definir a data de início (dia 2 do mês passado)
    if data_atual.month == 1:
        data_inicial = data_atual.replace(year=data_atual.year - 1, month=12, day=2)
    else:
        data_inicial = data_atual.replace(month=data_atual.month - 1, day=2)
    
    # Definir a data final (dia 2 do mês atual)
    data_final = data_atual.replace(day=2)

    # Filtrar os dados entre as datas
    df_filtrado = df[(df['data'] >= data_inicial) & (df['data'] < data_final)]

    # Calcular a soma da coluna 'valor'
    soma_valores = df_filtrado['valor'].sum()
    
    return soma_valores

def fatura_proxima(df):

    df = df.copy()

    # Obter a data atual
    data_atual = dt.datetime.today().date()

    # Definir a data de início (dia 2 do mês atual)
    data_inicial = data_atual.replace(day=2, month=data_atual.month + 1)
    
    # Definir a data final (dia 2 do mês seguinte)
    if data_atual.month == 12:
        data_final = data_inicial.replace(year=data_atual.year + 1, month=1, day=2)
    else:
        data_final = data_inicial.replace(month=data_inicial.month + 1, day=2)

    # Filtrar os dados entre as datas
    df_filtrado = df[(df['data'] >= data_inicial) & (df['data'] < data_final)]
    
    # Calcular a soma da coluna 'valor'
    soma_valores = df_filtrado['valor'].sum()
    return soma_valores

def proximas_faturas(df):

    df = df.copy()

    # Obter a data atual
    data_atual = dt.datetime.today().date()

    # Definir a data de início (dia 2 do mês atual)
    data_inicial = data_atual.replace(day=2, month=data_atual.month + 1)
    
    # Filtrar os dados entre as datas
    df_filtrado = df[(df['data'] >= data_inicial)]

    # Calcular a soma da coluna 'valor'
    soma_valores = df_filtrado['valor'].sum()
    
    return soma_valores

def soma_valores_por_classificacao(df):

    df = df.copy()

    # Group the data by month and year
    #df['mes'] = pd.to_datetime(df['data']).dt.to_period('M')
    df_grouped = df.groupby('classificacao')['valor'].sum()

    return df_grouped

def soma_valores_por_mes(df):

    df = df.copy()

    # Group the data by month and year
    df['mes'] = pd.to_datetime(df['data']).dt.to_period('M')
    df_grouped = df.groupby('mes')['valor'].sum()

    return df_grouped