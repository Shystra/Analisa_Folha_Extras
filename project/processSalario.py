import pandas as pd
import os

def processSalario(dfDirectory, select_columns):
    responseObjects = []
    
    for arquivo in os.listdir(dfDirectory):
        if arquivo.endswith('.xlsx') or arquivo.endswith('.xls'):
            caminho_completo = os.path.join(dfDirectory, arquivo)
            df = pd.read_excel(caminho_completo, sheet_name=0)
            responseObjects.append(df)

    responseObjectsConsolidado = pd.concat(responseObjects, ignore_index=True)
    responseObjectsConsolidado.columns = responseObjectsConsolidado.columns.str.strip()
    
    if select_columns:
        df_filtrado = responseObjectsConsolidado[select_columns]
    else:
        df_filtrado = responseObjectsConsolidado
    
    return df_filtrado

dfDirectory = "C:/Users/localuser/Documents/Lucas/Analise de Extras/Salario"
select_columns = [
    'Empresa', 'Matrícula', 'Nome', 'Função', 'Salário','Jornada Mensal Horas', 'Data de Admissão', 'Sit.'
]
df_filtrado = processSalario(dfDirectory, select_columns)
df_selected = df_filtrado[select_columns]
df_selected['Salário'] = pd.to_numeric(df_selected['Salário'], errors='coerce')
df_selected['Jornada Mensal Horas'] = pd.to_numeric(df_selected['Jornada Mensal Horas'], errors='coerce')
df_selected['MATRICULA | NOME COLABORADOR'] = df_selected['Matrícula'].astype(str) + " | " + df_selected['Nome']
# print(df_selected)

select_columns_salario = [
    'MATRICULA | NOME COLABORADOR', 'Função', 'Salário', 'Jornada Mensal Horas'
]
df_selectedAll = df_selected[select_columns_salario]
print(df_selectedAll)






# def processSalario(dfDirectory):
#     responseObjects = []
    
#     for arquivo in os.listdir(dfDirectory):
#         if arquivo.endswith('.xlsx') or arquivo.endswith('.xls'):
#             caminho_completo = os.path.join(dfDirectory, arquivo)
#             df = pd.read_excel(caminho_completo, sheet_name=0)
#             responseObjects.append(df)

#     responseObjectsConsolidado = pd.concat(responseObjects, ignore_index=True)
#     responseObjectsConsolidado.columns = responseObjectsConsolidado.columns.str.strip()
    
#     return responseObjectsConsolidado

# dfDirectory = "C:/Users/localuser/Documents/Lucas/Analise de Extras/Salario"
# df_consolidado = processSalario(dfDirectory)

# # Imprimir os nomes das colunas do DataFrame consolidado
# print(df_consolidado.columns)