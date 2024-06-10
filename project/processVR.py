import pandas as pd
import os

caminho_diretorio = "temp_dir_r09"
nome_arquivo = "VR.csv"

colunas = ['Nome', 'Valor do Benefício (R$)', 'Produto', 'CPF', 'Matrícula', 'Código Local Entrega', 'Local de Entrega', 'Código Departamento', 'Departamento', 'Emissão Cartão','Data', 'Recebido em', 'Assinatura']

def ler_csv_direto_e_limpar(caminho_diretorio, nome_arquivo):
    caminho_completo = os.path.join(caminho_diretorio, nome_arquivo)
    if os.path.exists(caminho_completo):
        df = pd.read_csv(caminho_completo, header=None, skiprows=1, names=colunas)
        
        df = df.dropna(how='all')
        
        
        # Remoção de linhas com valores específicos na coluna 'Nome'
        valores_a_excluir = ["Relatório de Detalhes do Pedido", "CNPJ:", "Razão Social:", "Pedido:", "Data do Pedido:", "Detalhes do Pedido", "Nome", "NaN" ]
        for valor in valores_a_excluir:
            df = df[~df['Nome'].str.contains(valor, na=False)]
        
        df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)
        
        df['Valor do Benefício (R$)'] = pd.to_numeric(df['Valor do Benefício (R$)'], errors='coerce')
        df['MATRICULA | NOME COLABORADOR'] = df['Nome'] + ' | ' + df['Matrícula'].astype(str)
        
        return df
    else:
        print(f"O arquivo {nome_arquivo} não foi encontrado em {caminho_diretorio}.")
        return None

df = ler_csv_direto_e_limpar(caminho_diretorio, nome_arquivo)

if df is not None:
    print(df)
    df.to_csv('VR_2023&2024-maio.csv', index=False)
else:
    print("DataFrame não disponível.")


# def ler_csv_direto(caminho_diretorio, nome_arquivo):
#     caminho_completo = os.path.join(caminho_diretorio, nome_arquivo)
#     if os.path.exists(caminho_completo):
#         # Se os nomes das colunas estiverem na linha 2 (index 1), ajuste skiprows para 1
#         df = pd.read_csv(caminho_completo, skiprows=1)
#         return df
#     else:
#         print(f"O arquivo {nome_arquivo} não foi encontrado em {caminho_diretorio}.")
#         return None

# df = ler_csv_direto(caminho_diretorio, nome_arquivo)

# if df is not None:
#     print(df)
# else:
#     print("DataFrame não disponível.")