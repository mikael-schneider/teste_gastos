import streamlit as st
import pandas as pd
from google.oauth2 import service_account
from googleapiclient.discovery import build


# ID da planilha
SPREADSHEET_ID = '1nScYWr4mI5FCpJGFv-6yjFmwcHEfcjQowg8dFc2XOBE'

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
def read_sheet(service, RANGE_NAME):
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME).execute()
    values = result.get('values', [])
    
    if not values:
        return pd.DataFrame()  # Retorna um DataFrame vazio se não houver dados

    # Converter os dados para um DataFrame
    df = pd.DataFrame(values[1:], columns=values[0])  # Usa a primeira linha como cabeçalho
    df['valor'] = df['valor'].replace({',': '.'}, regex=True).astype(float) # Corrige a vírgula
    df['data'] = pd.to_datetime(df['data'], format='%d/%m/%Y', errors='coerce').dt.date # Converte para data

    return df

def write_sheet(service, values_to_write, RANGE_NAME):
    sheet = service.spreadsheets()
    body = {'values': values_to_write}
    result = sheet.values().update(spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME, valueInputOption='RAW', body=body).execute()
    return result

def append_data(service, values, RANGE_NAME):
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