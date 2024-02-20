import pandas as pd
import os

# O caminho completo para o arquivo
nome_arquivo = "C:/Users/localuser/Documents/Lucas/Analise de Extras/R09/R09.xls"

def ler_arquivo_excel(nome_arquivo):
    if os.path.exists(nome_arquivo):
        # Usando read_excel para ler um arquivo do Excel
        df = pd.read_excel(nome_arquivo)
        
        # Remover linhas que são completamente nulas
        df = df.dropna(how='all')
        
        # Remover espaços em branco dos nomes das colunas
        df.columns = [col.strip() for col in df.columns]
        
        # Remover colunas específicas
        df = df.drop(columns=["Home Office", "Travado", "Email"])

        df['MATRICULA | NOME COLABORADOR'] = df["Nome"] + " | " + df['Código'].astype(str)
        
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
    df.to_csv('R09Test.csv', index=False)
else:
    print("DataFrame não disponível.")
