import pandas as pd
import os
from datetime import datetime, timedelta

# Função para processar os DataFrames
def processDF(dfDirectory, select_columns):
    responseObjects = []
    
    for arquivo in os.listdir(dfDirectory):
        if arquivo.endswith('.xlsx') or arquivo.endswith('.xls'):
            caminho_completo = os.path.join(dfDirectory, arquivo)
            df = pd.read_excel(caminho_completo, sheet_name=1)
            responseObjects.append(df)
    
    responseObjectConsolidado = pd.concat(responseObjects, ignore_index=True)
    responseObjectConsolidado.columns = responseObjectConsolidado.columns.str.strip()
    
    df_filtrado = responseObjectConsolidado[select_columns]
    return df_filtrado

# Função auxiliar para converter datetime.time para timedelta
def time_to_timedelta(time_val):
    if pd.isna(time_val):
        return pd.NaT
    return timedelta(hours=time_val.hour, minutes=time_val.minute)

# Definição dos diretórios e colunas
dfDirectory = "C:/Users/localuser/Documents/Lucas/Analise de Extras/DF"
select_columns = [
    'ID', 'MOTIVO', 'DATA EXECUÇÃO', 'NOME', 'MATRICULA', 'CARGO', 'POSTO', 
    'NOME.1', 'MATRICULA/ CPF', 'CARGO.1', 'DOBRA OU ESCALA / OPERAÇÃO', 'PERIODO'
]

# Processamento dos DataFrames
df_filtrado = processDF(dfDirectory, select_columns)
df_selected = df_filtrado[select_columns]
df_selected['MATRICULA | NOME COLABORADOR'] = df_selected['NOME.1'] + "-" + df_selected['MATRICULA/ CPF'].astype(str) 
# Extração e processamento das colunas INICIO e FIM
temp_df = df_selected['PERIODO'].str.extract(r'(\d{1,2}:\d{2})\s*.*?\s*(\d{1,2}:\d{2})')
temp_df.columns = ['INICIO', 'FIM']
df_selected = pd.concat([df_selected, temp_df], axis=1)

# Conversão para datetime.time e cálculo da duração
df_selected['INICIO_td'] = pd.to_datetime(df_selected['INICIO'], format='%H:%M', errors='coerce').apply(time_to_timedelta)
df_selected['FIM_td'] = pd.to_datetime(df_selected['FIM'], format='%H:%M', errors='coerce').apply(time_to_timedelta)
df_selected['DATA REFERENCIA'] = pd.to_datetime(df_selected['DATA EXECUÇÃO'], errors='coerce')
df_selected['DATA REFERENCIA'] = df_selected['DATA REFERENCIA'].dt.strftime('%B').str.upper()
df_selected['DURACAO'] = df_selected.apply(lambda row: ((row['FIM_td'] - row['INICIO_td']) + timedelta(days=1)) if row['FIM_td'] < row['INICIO_td'] else (row['FIM_td'] - row['INICIO_td']), axis=1)
df_selected['DURACAO_HORAS'] = df_selected['DURACAO'].dt.total_seconds() / 3600
df_selected['DURACAO_FORMATADA'] = df_selected['DURACAO'].apply(lambda x: '{:02d}:{:02d}'.format(int(x.total_seconds() // 3600), int((x.total_seconds() % 3600) // 60)) if not pd.isna(x) else '')

# Filtragem e seleção final das colunas
mask = df_selected['DOBRA OU ESCALA / OPERAÇÃO'].str.contains('HORA EXTRA|DOBRA', na=False)
df_filtered = df_selected[mask]

select_columns_cobertura = [
    'MATRICULA | NOME COLABORADOR', 'ID', 'DOBRA OU ESCALA / OPERAÇÃO', 'DATA EXECUÇÃO', 'PERIODO', 'INICIO', 'FIM', 'DURACAO_HORAS', 'DURACAO_FORMATADA', 'DATA REFERENCIA'
]

# Agora df_filtered pode ser acessado com a nova lista de colunas incluindo 'DURACAO_FORMATADA'
df_selectedAll = df_filtered[select_columns_cobertura]
df_selectedAll.to_csv('DFs_filtrado.csv', index=False)
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







