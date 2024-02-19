import pandas as pd
import os

def ler_csv_direto(caminho_diretorio, nome_arquivo):
    caminho_completo = os.path.join(caminho_diretorio, nome_arquivo)
    if os.path.exists(caminho_completo):
        df = pd.read_csv(caminho_completo)
        return df
    else:
        print(f"O arquivo {nome_arquivo} não foi encontrado em {caminho_diretorio}.")
        return None

def processFolha(caminho_diretorio, nome_arquivo):
    df = ler_csv_direto(caminho_diretorio, nome_arquivo)
    if df is not None:
        select_columns = ['Empresa', 'Matrícula', 'Nome', 'Data Referência', 'Tipo de Rubrica', 'Nome Ocorrência', 'Valor']
        df_selected = df[select_columns]

        df_selected['Valor'] = pd.to_numeric(df_selected['Valor'], errors='coerce')
        df_selected['Data Referência'] = pd.to_datetime(df_selected['Data Referência'], errors='coerce')
        df_selected['Mês'] = df_selected['Data Referência'].dt.strftime('%B').str.upper()
        df_selected['MATRICULA | NOME COLABORADOR'] = df_selected['Matrícula'].astype(str) + " | " + df_selected['Nome']
        mask = df_selected['Nome Ocorrência'].str.contains('Extras', na=False)
        df_filtered = df_selected[mask]

        select_columns_Folha = [
            'MATRICULA | NOME COLABORADOR', 'Tipo de Rubrica', 'Nome Ocorrência', 'Valor', 'Data Referência', 'Mês'
        ]
        df_selectedAll = df_filtered[select_columns_Folha]
        
        return df_selectedAll

caminho_diretorio = "temp_dir"
nome_arquivo = "Analise de Extras.csv"

df_processed = processFolha(caminho_diretorio, nome_arquivo)
if df_processed is not None:
    # Agrupar por colaborador e mês, e somar os valores
    df_grouped = df_processed.groupby(['MATRICULA | NOME COLABORADOR', 'Mês', 'Data Referência', 'Nome Ocorrência'], as_index=False)['Valor'].sum()
    print(df_grouped)
