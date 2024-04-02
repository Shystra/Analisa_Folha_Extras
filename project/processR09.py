import pandas as pd
import os
from datetime import timedelta

# O caminho completo para o arquivo
# nome_arquivo = "C:/Users/localuser/Documents/Lucas/Analise de Extras/temp_dir_Compact_R09/R09.csv"
nome_arquivo = 'temp_dir_r09/r09-sucesso-01-01-2024-a-31-03-2024-mnmb62iwdd.xls'

def time_to_timedelta(time_val):
    if pd.isna(time_val):
        return pd.NaT
    return timedelta(hours=time_val.hour, minutes=time_val.minute)

def ler_arquivo_excel(nome_arquivo):
    print("Executando...")
    if os.path.exists(nome_arquivo):
        df = pd.read_excel(nome_arquivo)
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
        
        return df
    else:
        print(f"O arquivo {nome_arquivo} não foi encontrado.")
        return None

df = ler_arquivo_excel(nome_arquivo)

if df is not None:
    print(df.columns)
    print(df)
    df.to_csv('JAN_MAR-2024.csv', index=False)
else:
    print("DataFrame não disponível.")
