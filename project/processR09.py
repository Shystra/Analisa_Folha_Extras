import pandas as pd
import os

# O caminho completo para o arquivo
nome_arquivo = "C:/Users/localuser/Documents/Lucas/Analise de Extras/R09/R09.xls"

def time_to_timedelta(time_val):
    if pd.isna(time_val):
        return pd.NaT
    return timedelta(hours=time_val.hour, minutes=time_val.minute)


def ler_arquivo_excel(nome_arquivo):
    if os.path.exists(nome_arquivo):
        # Usando read_excel para ler um arquivo do Excel
        df = pd.read_excel(nome_arquivo)
        
        # Remover linhas que são completamente nulas
        df = df.dropna(how='all')
        
        # Remover espaços em branco dos nomes das colunas
        df.columns = [col.strip() for col in df.columns]
        
        # Remover colunas específicas
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
        # df['Entrada'] = pd.to_datetime(df['Entrada'], format='%H:%M', errors='coerce').apply(time_to_timedelta)
        # df['Pausa'] = pd.to_datetime(df['Pausa'], format='%H:%M', errors='coerce').apply(time_to_timedelta)
        # df['Retorno'] = pd.to_datetime(df['Retorno'], format='%H:%M', errors='coerce').apply(time_to_timedelta)
        # df['Saída'] = pd.to_datetime(df['Saída'], format='%H:%M', errors='coerce').apply(time_to_timedelta)
        
        return df
    else:
        print(f"O arquivo {nome_arquivo} não foi encontrado.")
        return None

# Chama a função e atribui o resultado a 'df'
df = ler_arquivo_excel(nome_arquivo)

# Verifica se 'df' não é None antes de imprimir
if df is not None:
    print(df.columns)
    print(df)
    # df.to_csv('R09Test.csv', index=False)
else:
    print("DataFrame não disponível.")
