import pandas as pd
import os



pgtMentoreDirectory = "C:/Users/localuser/Documents/Lucas/Analise de Extras/Pgt Mentore"

def processDF (dfDirectory, select_columns):
    responseObjects = []
    
    # Iterar sobre cada arquivo no diretório especificado
    for arquivo in os.listdir(dfDirectory):
        if arquivo.endswith('.xlsx') or arquivo.endswith('.xls'):
            caminho_completo = os.path.join(dfDirectory, arquivo)
            df = pd.read_excel(caminho_completo, sheet_name=1)
            responseObjects.append(df)
    

    responseObjectConsolidado = pd.concat(responseObjects, ignore_index=True)
    responseObjectConsolidado.columns = responseObjectConsolidado.columns.str.strip()
    
    df_filtrado = responseObjectConsolidado[select_columns]
    return df_filtrado

dfDirectory = "C:/Users/localuser/Documents/Lucas/Analise de Extras/DF"
select_columns = [
    'ID', 'MOTIVO', 'DATA EXECUÇÃO', 'NOME', 'MATRICULA', 'CARGO', 'POSTO', 
    'NOME.1', 'MATRICULA/ CPF', 'CARGO.1', 'DOBRA OU ESCALA / OPERAÇÃO'
]

df_filtrado = processDF(dfDirectory, select_columns)
df_selected = df_filtrado[select_columns]
df_selected['MATRICULA | NOME COLABORADOR'] = df_selected['MATRICULA/ CPF'].astype(str) + " | " + df_selected['NOME.1']
# print(df_selected)
mask = df_selected['DOBRA OU ESCALA / OPERAÇÃO'].str.contains('HORA EXTRA|DOBRA')
df_filtered = df_selected[mask]
select_columns_cobertura = [
    'MATRICULA | NOME COLABORADOR', 'ID', 'DOBRA OU ESCALA / OPERAÇÃO', 'DATA EXECUÇÃO', 
]

df_selectedAll = df_filtered[select_columns_cobertura]
print(df_selectedAll)




















# def processFolhaDirectory(folhaDirectory):
#     responseObjects = []

#     # Iterar sobre cada arquivo no diretório especificado
#     for arquivo in os.listdir(folhaDirectory):
#         if arquivo.endswith('.xlsx') or arquivo.endswith('.xls'):
#             caminho_completo = os.path.join(folhaDirectory, arquivo)
#             df = pd.read_excel(caminho_completo, sheet_name=0)
#             responseObjects.append(df)

#     responseObjectConsolidado = pd.concat(responseObjects, ignore_index=True)
#     responseObjectConsolidado.columns = responseObjectConsolidado.columns.str.strip()
    
#     return responseObjectConsolidado


# folhaDirectory = "C:/Users/localuser/Documents/Lucas/Analise de Extras/Folha"
# df_filtradoFolha = processFolhaDirectory(folhaDirectory)


# print(df_filtradoFolha)







