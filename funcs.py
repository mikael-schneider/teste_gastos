import datetime as dt
import pandas as pd

def formatar_valor_brasileiro(valor):
    valor_str = f"{valor:,.2f}"
    valor_str = valor_str.replace(",", "X").replace(".", ",").replace("X", ".")
    return valor_str

def ano_atual():

    return dt.datetime.today().year

def saldo_atual(df):

    df = df.copy()

    # Calcular a soma da coluna 'valor'
    soma_proventos = df['proventos'].sum()
    soma_debitos = df['debitos'].sum()

    saldo_atual = soma_proventos - soma_debitos
    
    return saldo_atual

def saldo_emprestado(df):

    df = df.copy()

    # Calcular a soma da coluna 'emprestimo'
    soma_emprestimo = df['emprestimos'].sum()
    soma_devolucao = df['devolucoes'].sum()

    saldo_emprestado = soma_emprestimo - soma_devolucao

    return saldo_emprestado

def saldo_total_indisponivel(df):

    df = df.copy()

    saldo_atual = df['proventos'].sum() - df['debitos'].sum()
    saldo_emprestado = df['emprestimos'].sum() - df['devolucoes'].sum()

    saldo_total_indisponivel = saldo_atual + saldo_emprestado

    return saldo_total_indisponivel

def deb_previsto(df):

    df = df.copy()
    deb_previsto = df['deb_previsto'].sum()

    return deb_previsto

def prov_previsto(df):
    
        df = df.copy()
        prov_previsto = df['prov_previsto'].sum()
    
        return prov_previsto

def df_mes_atual(df):

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

    return df_filtrado

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