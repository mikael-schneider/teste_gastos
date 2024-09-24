import streamlit as st
import pandas as pd
from google.oauth2 import service_account
from googleapiclient.discovery import build

# ID da planilha
SPREADSHEET_ID = '1nScYWr4mI5FCpJGFv-6yjFmwcHEfcjQowg8dFc2XOBE'
RANGE_NAME = 'gastosmika'  # Alterado para a aba sem intervalo específico

# Autenticação via conta de serviço
def authenticate_gsheets():
    creds = service_account.Credentials.from_service_account_info(
        st.secrets["google_api"]
    )
    return creds

# Conectar ao Google Sheets
def get_service():
    creds = authenticate_gsheets()
    service = build('sheets', 'v4', credentials=creds)
    return service

# Funções para ler e escrever na planilha
def read_sheet(service):
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME).execute()
    values = result.get('values', [])
    
    if not values:
        st.warning("Nenhum dado encontrado na planilha.")
        return pd.DataFrame()  # Retorna um DataFrame vazio se não houver dados

    # Converter os dados para um DataFrame
    df = pd.DataFrame(values[1:], columns=values[0])  # Usa a primeira linha como cabeçalho
    return df

def write_sheet(service, values_to_write):
    sheet = service.spreadsheets()
    body = {'values': values_to_write}
    result = sheet.values().update(spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME,
                                   valueInputOption='RAW', body=body).execute()
    return result

def append_data(service, values):
    # Prepara o corpo da requisição
    body = {
        'values': [values]  # Adicione a nova linha aqui
    }
    # Chama a API para adicionar os dados
    result = service.spreadsheets().values().append(
        spreadsheetId=SPREADSHEET_ID,
        range=RANGE_NAME,
        valueInputOption='RAW',
        body=body
    ).execute()

    print(f"{result.get('updates').get('updatedCells')} células atualizadas.")

# Interface do Streamlit
def main():
    st.title("Aplicação Streamlit com Google Sheets")

    service = get_service()

    if st.button('Carregar dados da planilha'):
        data = read_sheet(service)
        st.write("Dados da planilha:", data)

    st.subheader("Inserir novos dados")
    nome = st.text_input("Nome")
    idade = st.number_input("Idade", min_value=1, max_value=120, step=1)

    if st.button("Salvar dados"):
        if nome and idade:
            new_data = [nome, str(idade)]  # Ajuste para uma lista simples
            append_data(service, new_data)  # Passar a nova linha para a função
            st.success("Dados salvos com sucesso!")

if __name__ == '__main__':
    main()
