import pandas as pd
import os

caminho_diretorio = "./Folha"
nome_arquivo = "SEGURANCA_01-2024.xlsx"

def ler_arquivo_excel(caminho_diretorio, nome_arquivo):
    print('Lendo arquivo Excel')
    caminho_completo = os.path.join(caminho_diretorio, nome_arquivo)
    if os.path.exists(caminho_completo):
        df = pd.read_excel(caminho_completo)  # Assegure-se de que o arquivo é um Excel. Para CSV, use pd.read_csv
        return df
    else:
        print(f"O arquivo {nome_arquivo} não foi encontrado em {caminho_diretorio}.")
        return None

def processFolha(caminho_diretorio, nome_arquivo):
    print('Começando ProcessFolha')
    df = ler_arquivo_excel(caminho_diretorio, nome_arquivo)  # Ajuste conforme a função corrigida
    if df is not None:
        select_columns = ['Empresa', 'Matrícula', 'Nome', 'Data Referência', 'Tipo de Rubrica', 'Nome Ocorrência', 'Valor']
        df_selected = df[select_columns]

        df_selected['Valor'] = pd.to_numeric(df_selected['Valor'], errors='coerce')
        df_selected['Data Referência'] = pd.to_datetime(df_selected['Data Referência'], errors='coerce')
        df_selected['Mês'] = df_selected['Data Referência'].dt.strftime('%B').str.upper()
        df_selected['MATRICULA | NOME COLABORADOR'] = df_selected['Nome'] + " | " + df_selected['Matrícula'].astype(str)
        mask = df_selected['Nome Ocorrência'].str.contains('Zipdin', na=False)
        df_filtered = df_selected[mask]

        select_columns_Folha = [
            'MATRICULA | NOME COLABORADOR', 'Tipo de Rubrica', 'Nome Ocorrência', 'Valor', 'Data Referência', 'Mês'
        ]
        df_selectedAll = df_filtered[select_columns_Folha]
        
        return df_selectedAll

# Processamento principal
df_processed = processFolha(caminho_diretorio, nome_arquivo)
if df_processed is not None:
    # Salva o dataframe processado em um arquivo CSV
    df_processed.to_csv('SEGURANCA_01-2024.csv', index=False)
    print(df_processed)
