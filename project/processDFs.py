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
    'NOME.1', 'MATRICULA/ CPF', 'CARGO.1', 'DOBRA OU ESCALA / OPERAÇÃO', 'PERIODO'
]

df_filtrado = processDF(dfDirectory, select_columns)
df_selected = df_filtrado[select_columns]
df_selected['MATRICULA | NOME COLABORADOR'] = df_selected['MATRICULA/ CPF'].astype(str) + " | " + df_selected['NOME.1']
# print(df_selected)




temp_df = df_selected['PERIODO'].str.extract(r'(\d{1,2}:\d{2})\s*.*?\s*(\d{1,2}:\d{2})')
while len(temp_df.columns) < 2:
    temp_df[len(temp_df.columns)] = pd.NA
temp_df.columns = ['INICIO', 'FIM']


df_selected = pd.concat([df_selected, temp_df], axis=1)

mask_invalid_inicio = ~df_selected['INICIO'].str.match(r'^\d{1,2}:\d{2}$', na=False)
mask_invalid_fim = ~df_selected['FIM'].str.match(r'^\d{1,2}:\d{2}$', na=False)


df_selected.loc[mask_invalid_inicio, 'INICIO'] = pd.NA
df_selected.loc[mask_invalid_fim, 'FIM'] = pd.NA

df_selected['INICIO'] = pd.to_datetime(df_selected['INICIO'], format='%H:%M', errors='coerce').dt.time
df_selected['FIM'] = pd.to_datetime(df_selected['FIM'], format='%H:%M', errors='coerce').dt.time


mask = df_selected['DOBRA OU ESCALA / OPERAÇÃO'].str.contains('HORA EXTRA|DOBRA', na=False)
df_filtered = df_selected[mask]
select_columns_cobertura = [
    'MATRICULA | NOME COLABORADOR', 'ID', 'DOBRA OU ESCALA / OPERAÇÃO', 'DATA EXECUÇÃO', 'PERIODO', 'INICIO', 'FIM'
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







