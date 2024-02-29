import pandas as pd
import os

caminho_diretorio = "temp_dir_Compact_FeriasGozadas"
nome_arquivo = "FeriasGozadas.csv"

def ler_csv_direto(caminho_diretorio, nome_arquivo):
    caminho_completo = os.path.join(caminho_diretorio, nome_arquivo)
    if os.path.exists(caminho_completo):
        try:
            # Substitua o delimitador aqui pelo que você descobrir ser o correto
            df = pd.read_csv(caminho_completo, delimiter=',')
            return df
        except Exception as e:
            print(f"Erro ao ler o arquivo {nome_arquivo}: {e}")
            return None
    else:
        print(f"O arquivo {nome_arquivo} não foi encontrado em {caminho_diretorio}")
        return None

def processFeriasGozadas(caminho_diretorio, nome_arquivo):
    df = ler_csv_direto(caminho_diretorio, nome_arquivo)
    
    if df is not None:
    
        # Ajuste das colunas
        df = df.iloc[:, :18]
        df.columns = [
            'Coluna0', 'Rateio', 'Matricula', 'Nome', 'Vencidos', 'Proporcionais',
            'Ampliada', 'Gozadostest', 'Coluna10', 'Coluna11', 'Coluna12',
            'Coluna13', 'Coluna14', 'Data Retirada', 'Data Saída', 'test',
            'Gozados Qtd', 'Coluna19',
        ]
        
        # Conversão para numérico e datetime
        # df['Gozados Qtd'] = pd.to_numeric(df['Gozados Qtd'], errors='coerce')
        df['Data Retirada'] = df['Data Retirada'].fillna(df['Data Saída'])
        df['Data Retirada'] = pd.to_datetime(df['Data Retirada'], errors='coerce', dayfirst=True).dt.strftime('%d/%m/%Y')
        df['Data Saída'] = pd.to_datetime(df['Data Saída'], errors='coerce', dayfirst=True).dt.strftime('%d/%m/%Y')
        
        # # Criação e formatação da coluna 'Data Fim'
        # df['Data Fim'] = df['Data Saída'] + pd.to_timedelta(df['Gozados Qtd'], unit='D')
        # df['Data Fim'] = df['Data Fim'].dt.strftime('%d/%m/%Y')
        
        # Remoção de colunas desnecessárias
        colunas_para_remover = [
            'Coluna0', 'Vencidos', 'Proporcionais', 
            'Gozadostest', 'Coluna10', 'Coluna11', 'Coluna12', 'Coluna13',
            'Coluna14',  'Coluna19',
        ]
        # Encontrar linhas onde a coluna 'nome' é não nula, mas todas as outras colunas são nulas
        mask = df['Matricula'].notnull() & df.drop(columns='Matricula').isnull().all(axis=1)
       
        df = df.dropna(how='all')
        df.reset_index(drop=True, inplace=True)

        df = df[~mask]
        df = df.drop(colunas_para_remover, axis=1)
        
        # Preenchimento condicional de 'Nome' e 'Matricula'
        for i in range(1, len(df)):
            if pd.notna(df.at[i, 'Ampliada']):
                df.at[i, 'Nome'] = df.at[i-1, 'Nome']
                df.at[i, 'Matricula'] = df.at[i-1, 'Matricula']
                df.at[i, 'Rateio'] = df.at[i-1, 'Rateio']
        # df['Matricula'] = df['Matricula'].ffill()
        # df['Nome'] = df['Nome'].ffill()
        
        return df
            
                

        
    
    

df_integrado = processFeriasGozadas(caminho_diretorio, nome_arquivo)
if df_integrado is not None:
    print(df_integrado)
    print(df_integrado.columns)
    df_integrado.to_csv("teste.csv", index=False, sep=';')
