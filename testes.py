import datetime as dt

def tratar_dados(dia: int, mes: int, descricao: str, valor: float, parcelas: int, classificacao: str):
    """
    Função para dividir um valor em parcelas e retornar uma lista com os dados das parcelas.

    Parâmetros:
    dia (int): O dia do vencimento.
    mes (int): O mês do vencimento.
    descricao (str): Descrição do gasto.
    valor (float): O valor total.
    parcelas (int): Número de parcelas.
    classificacao (str): Classificação do gasto.

    Retorna:
    list: Lista de parcelas com data, descrição, valor por parcela, número de parcelas e classificação.
    """
    dados = []
    
    ano = dt.datetime.today().year
    
    for i in range(parcelas):
        
        # Cálculo para o mês atual, levando em consideração que pode passar de 12 (próximo ano)
        mes_parcela = (mes + i - 1) % 12 + 1
        ano_parcela = ano + (mes + i - 1) // 12  # Incrementa o ano se o mês passar de 12

        # Formatação da descrição e valores para cada parcela
        descricao_parcela = f'{i+1}/{parcelas} {descricao}'
        valor_parcela = float(valor) / parcelas
        
        # Adiciona os dados formatados para cada parcela na lista
        dados.append([f'{dia}/{mes_parcela}/{ano_parcela}', descricao_parcela, valor_parcela, parcelas, classificacao])

    return dados

# Testando a função
resultado = tratar_dados(1, 12, 'Teste', 100, 3, 'Teste')
print(resultado)
