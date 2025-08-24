# from datetime import *
# import pandas as pd
# from openpyxl.workbook import Workbook

# from db import criar, selecionar_todas_as_compras

# dados = selecionar_todas_as_compras()

# df = pd.DataFrame(dados, columns=['ID', 'DATA_DA_COMPRA', 'DATA_DO_VENCIMENTO', 'CREDOR', 'PARCELAS', 'VALOR', 'CLASSIFICACAO', 'CENTRO_DE_CUSTO', 'BANCO'])
# print(df.head())
# arquivo_excell = 'compras.xlsx'
# df.to_excel(arquivo_excell, index=False)
# print(f"Dados exportados para {arquivo_excell} com sucesso!")   


# data = datetime.now()

# def gerar_parcelas(data, parcelas):
#     for i in range(1, parcelas + 1):
#         data_da_compra = data + timedelta(days=30 * i)
#         vencimento = data_da_compra.strftime("%d/%m/%Y")
#         print(f"Parcela {i}/{parcelas}: Vencimento em {vencimento}")

# def salvar_parcelas():
#     try:
#         valor = float(input("Digite o valor da compra: "))
#         parcelas = int(input("Digite o número de parcelas: "))
#         credor = input("Digite o nome do credor: ")
#         classificacao = input("Digite a classificação da compra: ")
#         centro_de_custo = input("Digite o centro de custo: ")

        
#         for i in range(1, parcelas + 1):
#             data_da_compra = data + timedelta(days=30 * i)
#             vencimento = data_da_compra.strftime("%d/%m/%Y")
#             valor_parcela = valor / parcelas
#             criar(data.strftime("%d/%m/%Y"), vencimento, credor, f"{i}/{parcelas}", valor_parcela, classificacao, centro_de_custo)

#         print("Parcelas salvas com sucesso!")
#     except Exception as e:
#         print(f"Erro ao salvar parcelas: {e}")

# def listar_anos():
#     ano = 2025
#     for i in range(0, 100):
#         print(ano + i)
from num2words import num2words

def valor_por_extenso(valor):
    valor = round(float(valor), 2)
    reais = int(valor)
    centavos = int(round((valor - reais) * 100))

    extenso_reais = num2words(reais, lang='pt_BR').replace(',', ' e ')
    extenso_centavos = num2words(centavos, lang='pt_BR')

    resultado = f"{extenso_reais} reais"
    if centavos > 0:
        resultado += f" e {extenso_centavos} centavos"
    return resultado

# Exemplo de uso
valor_digitado = "10000.32"
print(valor_por_extenso(valor_digitado))



