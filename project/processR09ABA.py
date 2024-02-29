import pandas as pd
import os
from datetime import timedelta
import openpyxl  # Importa a biblioteca openpyxl

nome_arquivo = "C:/Users/localuser/Documents/Lucas/Analise de Extras/temp_dir_Compact_R09/R09.xlsx"

def time_to_timedelta(time_val):
    if pd.isna(time_val):
        return pd.NaT
    return timedelta(hours=time_val.hour, minutes=time_val.minute)

def ler_e_limpar_abas(nome_arquivo):
    print("Executando...")
    if os.path.exists(nome_arquivo):
        # Carrega o arquivo Excel
        wb = openpyxl.load_workbook(nome_arquivo)
        sheet_names = wb.sheetnames  # Obtém os nomes de todas as abas
        
        # Itera por cada aba para ler e limpar os dados
        for sheet_name in sheet_names:
            df = pd.read_excel(nome_arquivo, sheet_name=sheet_name)
            df = df.dropna(how='all')
            df.columns = [col.strip() for col in df.columns]
            df = df.drop(columns=[
                "Home Office", 
                "Travado", 
                "Email", 
                "Entrada Local",
                "Pausa Local",
                "Retorno Local",
                "Entrada GPS",
                "Pausa GPS",
                "Retorno GPS"
            ])
            df['MATRICULA | NOME COLABORADOR'] = df["Nome"] + " | " + df['Código'].astype(str)
            df['Entrada'] = pd.to_datetime(df['Entrada'], format='%H:%M', errors='coerce').apply(time_to_timedelta)
            df['Pausa'] = pd.to_datetime(df['Pausa'], format='%H:%M', errors='coerce').apply(time_to_timedelta)
            df['Retorno'] = pd.to_datetime(df['Retorno'], format='%H:%M', errors='coerce').apply(time_to_timedelta)
            df['Saída'] = pd.to_datetime(df['Saída'], format='%H:%M', errors='coerce').apply(time_to_timedelta)
            
            # Aqui você pode salvar os dados limpos em um novo arquivo ou em uma nova aba
            # Por exemplo, vamos apenas imprimir o nome da aba e as primeiras linhas do DataFrame limpo
            print(f"Aba: {sheet_name}")
            print(df.head())

        # Fechar o arquivo Excel
        wb.close()
    else:
        print(f"O arquivo {nome_arquivo} não foi encontrado.")

ler_e_limpar_abas(nome_arquivo)
