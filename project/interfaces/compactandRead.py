import pandas as pd
import os
import zipfile
from datetime import datetime

def extrair_data_do_nome_arquivo(nome_arquivo):
    # Extrair a substring que contém a data
    partes = nome_arquivo.split('_')
    if len(partes) > 1:
        data_str = partes[1][:8]  # Assume que a data está no formato AAAAMMDD
        try:
            # Converter a string para um objeto datetime
            return datetime.strptime(data_str, '%Y%m%d').date()
        except ValueError:
            return None
    return None

def consolidar_e_salvar(folhaDirectory, arquivo_saida):
    responseObjects = []

    for arquivo in os.listdir(folhaDirectory):
        if arquivo.endswith('.xlsx') or arquivo.endswith('.xls'):
            caminho_completo = os.path.join(folhaDirectory, arquivo)
            data_referencia = extrair_data_do_nome_arquivo(arquivo)
            
            if data_referencia:
                df = pd.read_excel(caminho_completo, sheet_name=0)
                # Adicionar a data de referência como uma nova coluna
                df['Data de Referência'] = data_referencia
                responseObjects.append(df)

    if responseObjects:
        df_consolidado = pd.concat(responseObjects, ignore_index=True)

        # Salvar o DataFrame consolidado em um arquivo CSV para compatibilidade
        csv_path = arquivo_saida + ".csv"
        df_consolidado.to_csv(csv_path, index=False)

        # Compactar o arquivo CSV em um arquivo ZIP
        with zipfile.ZipFile(arquivo_saida + ".zip", 'w', zipfile.ZIP_DEFLATED) as zipf:
            zipf.write(csv_path, os.path.basename(csv_path))
        
        # Opcional: remover o arquivo CSV após a compressão
        os.remove(csv_path)

        print(f"Arquivo consolidado salvo e compactado como: {arquivo_saida}.zip")
    else:
        print("Nenhum arquivo válido encontrado para processamento.")

# Definir o diretório e o nome do arquivo de saída
# Exemplo de uso
folhaDirectory = "C:/Users/localuser/Documents/Lucas/Analise de Extras/VR"
arquivo_saida = "C:/Users/localuser/Documents/Lucas/Analise de Extras/VR"
consolidar_e_salvar(folhaDirectory, arquivo_saida)
