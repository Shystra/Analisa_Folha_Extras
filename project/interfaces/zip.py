import pandas as pd
import zipfile
import os

def ler_dados_consolidados(arquivo_zip):
    # Criar um diretório temporário se não existir
    temp_dir = "temp_dir_r09"
    os.makedirs(temp_dir, exist_ok=True)
    
    with zipfile.ZipFile(arquivo_zip, 'r') as zipf:
        zipf.extractall(temp_dir)  # Extrair para o diretório temporário
        for arquivo in zipf.namelist():
            caminho_completo = os.path.join(temp_dir, arquivo)
            df = pd.read_csv(caminho_completo)
            # Opcional: remover o diretório temporário e seu conteúdo após a leitura
            # os.remove(caminho_completo)
        # os.rmdir(temp_dir)  # Remover o diretório temp_dir, certifique-se de que está vazio
    return df

# arquivo_zip = "C:/Users/localuser/Documents/Lucas/Analise de Extras/FeriasGozadas.zip"C:\Users\localuser\Documents\joao\Planilhas\TEMP PLAN BOT
arquivo_zip = 'C:/Users/localuser/Documents/joao/Planilhas/VR.zip'

df = ler_dados_consolidados(arquivo_zip)


print(df)
