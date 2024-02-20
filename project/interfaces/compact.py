import pandas as pd
import os
import zipfile

def consolidar_e_salvar(folhaDirectory, arquivo_saida):
    responseObjects = []

    for arquivo in os.listdir(folhaDirectory):
        if arquivo.endswith('.xlsx') or arquivo.endswith('.xls'):
            caminho_completo = os.path.join(folhaDirectory, arquivo)
            df = pd.read_excel(caminho_completo, sheet_name=0)
            responseObjects.append(df)

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

# Definir o diretório e o nome do arquivo de saída
# folhaDirectory = "C:/Users/localuser/Documents/Lucas/Analise de Extras/Folha"
folhaDirectory = "C:/Users/localuser/Documents/Lucas/Analise de Extras/VR"
arquivo_saida = "C:/Users/localuser/Documents/Lucas/Analise de Extras"

consolidar_e_salvar(folhaDirectory, arquivo_saida)
