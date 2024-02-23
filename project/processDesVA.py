import pandas as pd
import os


caminho_diretorio = "temp_dir_ferias"
nome_arquivo = "Folha.csv"

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
        # df_selected['MATRICULA | NOME COLABORADOR'] = df_selected['Matrícula'].astype(str) + " | " + df_selected['Nome']
        df_selected['MATRICULA | NOME COLABORADOR'] =  df_selected['Nome'] + " | " + df_selected['Matrícula'].astype(str)
        mask = df_selected['Nome Ocorrência'].str.contains('Desc. Devolução de VA', na=False)
        df_filtered = df_selected[mask]

        select_columns_Folha = [
            'MATRICULA | NOME COLABORADOR', 'Tipo de Rubrica', 'Nome Ocorrência', 'Valor', 'Data Referência', 'Mês'
        ]
        df_selectedAll = df_filtered[select_columns_Folha]
        
        return df_selectedAll


def ler_salarios():
    df_salarios = pd.read_csv('salarios_colaboradores.csv')
    return df_salarios


def integrar_dados_folha_com_salario(df_folha, df_salarios):
    # Fusão dos dataframes com base na coluna 'MATRICULA | NOME COLABORADOR'
    df_integrado = pd.merge(df_folha, df_salarios, on='MATRICULA | NOME COLABORADOR', how='left')
    return df_integrado


df_salarios = ler_salarios()
df_processed = processFolha(caminho_diretorio, nome_arquivo)
if df_processed is not None and df_salarios is not None:
    df_integrado = integrar_dados_folha_com_salario(df_processed, df_salarios)
    df_integrado.to_csv('DescVA.csv', index=False)
    print(df_integrado)





