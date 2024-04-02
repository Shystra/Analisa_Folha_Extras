import pandas as pd
import os
import openpyxl
from openpyxl.utils.dataframe import dataframe_to_rows

def consolidar_e_salvar(folhaDirectory, arquivo_saida_base):
    print("Executando...")
    responseObjects = []

    for arquivo in os.listdir(folhaDirectory):
        caminho_completo = os.path.join(folhaDirectory, arquivo)
        if arquivo.endswith('.xls') or arquivo.endswith('.xlsx'):
            engine = 'openpyxl' if arquivo.endswith('.xlsx') else None
            try:
                df = pd.read_excel(caminho_completo, engine=engine)
                responseObjects.append(df)
            except Exception as e:
                print(f"Erro ao ler o arquivo {arquivo}: {e}")
        else:
            continue

    if responseObjects:
        df_consolidado = pd.concat(responseObjects, ignore_index=True)

        max_rows_per_sheet = 1048576
        file_count = 1
        row_accumulator = 0

        # Cria a primeira pasta de trabalho do Excel
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Sheet1"

        for r in dataframe_to_rows(df_consolidado, index=False, header=True):
            if row_accumulator >= max_rows_per_sheet:
                # Salva a pasta de trabalho atual e cria uma nova
                wb.save(f"{arquivo_saida_base}_{file_count}.xlsx")
                file_count += 1
                row_accumulator = 0  # Reinicia o contador de linhas

                # Cria uma nova pasta de trabalho do Excel
                wb = openpyxl.Workbook()
                ws = wb.active
                ws.title = "Sheet1"

            ws.append(r)
            row_accumulator += 1

        # Salva a última pasta de trabalho criada
        wb.save(f"{arquivo_saida_base}_{file_count}.xlsx")

        print("Encerrou o processo...")
        print(f"Arquivos consolidados salvos com o base: {arquivo_saida_base}")
    else:
        print("Nenhum arquivo Excel válido foi encontrado para processamento.")

# Definir o diretório e o nome do arquivo de saída base (sem a extensão)
#folhaDirectory = "C:/Users/localuser/Documents/Lucas/Analise de Extras/R09"
folhaDirectory = "temp_dir_r09"        
arquivo_saida_base = "C:/Users/localuser/Documents/joao/Planilhas/TEMP PLAN BOT"

consolidar_e_salvar(folhaDirectory, arquivo_saida_base)
