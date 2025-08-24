from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import QMessageBox, QFileDialog
from datetime import *
import pandas as pd
from openpyxl.workbook import Workbook
from db import criar, somar_valores, selecionar_todas_as_compras, criar_credor, listar_credor, criar_classificacao, listar_classificacao, criar_centro_de_custo, listar_centro_de_custo, selecionar_compras_mes_ano, criar_fatura, selecionar_fatura

import requests

valores = somar_valores()


data = datetime.now()

anos = [str(2025 + i) for i in range(100)]  # Lista de anos de 2025 a 2124

def msg_info(msg):
    QMessageBox.information(None, "Sucesso", msg)

def msg_warning(msg):
    QMessageBox.warning(None, "Erro", msg)

def open_form_listar_lancamentos():
    frm_listar_lancamentos.show()

# formulario para adicionar lançamentos
def frm_lancar_ar():
    frm_lancar_ars.show()
    frm_lancar_ars.comboBox.clear() 
    frm_lancar_ars.cmbClassificacao.clear()
    frm_lancar_ars.cmbCentroCusto.clear()  # Limpa os campos antes de adicionar
     # Limpa os itens antes de adicionar
    credores = listar_credor()
    classificacoes = listar_classificacao()
    centros = listar_centro_de_custo()

    for credor in credores:  # Assuming the second column is the name of the creditor
        frm_lancar_ars.comboBox.addItems([credor[1]])
    
    for classificacao in classificacoes:
        frm_lancar_ars.cmbClassificacao.addItems([classificacao[1]]) 
    
    for centro in centros:
        frm_lancar_ars.cmbCentroCusto.addItems([centro[1]])  # Assuming the second column is the name of the center
         # Assuming the second column is the name of the creditor
   
def salvar_parcelas():
    try:
        valor = float(frm_lancar_ars.txtValor.text())
        parcelas = int(frm_lancar_ars.txtParcelas.text())
        credor = frm_lancar_ars.comboBox.currentText()
        classificacao = frm_lancar_ars.cmbClassificacao.currentText()
        centro_de_custo = frm_lancar_ars.cmbCentroCusto.currentText()
        banco = frm_lancar_ars.cmbBanco.currentText() # Assuming you have a field for the bank
        for i in range(1, parcelas + 1):
            data_da_compra = data + timedelta(days=30 * i)
            vencimento = data_da_compra.strftime("%d/%m/%Y")
            valor_parcela = valor / parcelas
            frm_lancar_ars.txtValorParcela.setText(f"{valor_parcela:.2f}")  # This will print the value entered in the txtValor field
            criar(data.strftime("%d/%m/%Y"), vencimento, credor, f"{i}/{parcelas}", valor_parcela, classificacao, centro_de_custo, banco)  
        
        frm_lancar_ars.txtValor.clear()
        frm_lancar_ars.txtParcelas.clear()
        frm_lancar_ars.comboBox.clear()
        frm_lancar_ars.cmbClassificacao.clear()
        frm_lancar_ars.cmbCentroCusto.clear()
        frm_lancar_ars.txtValorParcela.clear()

        listar_lancamentos(frm_listar_lancamentos)
        frm_listar_lancamentos.lblValor.setText(f"R$ {somar_valores():.2f}")


        msg_info("Parcelas salvas com sucesso!")
    except Exception as e:
        msg_warning(f"Erro ao salvar parcelas: {e}")
   
def listar_lancamentos(fomulario):  
    dados = selecionar_todas_as_compras()
    frm_listar_lancamentos.txtPesquisaAno.addItems(anos)
    frm_listar_lancamentos.lblValor.setText(f"R$ {valores:.2f}")
    fomulario.tabelaLancamentos.setRowCount(len(dados))
    fomulario.tabelaLancamentos.setColumnCount(9)

    for linha in range(len(dados)):
        for coluna in range(0, 9):
            fomulario.tabelaLancamentos.setItem(linha, coluna, QtWidgets.QTableWidgetItem(str(dados[linha][coluna])))
        
    fomulario.tabelaLancamentos.setHorizontalHeaderLabels(['ID', 'Data do Lançamento', 'Data do Vencimento', 'Credor', 'Parcelas', 'Valor', 'Classificação', 'Centro de Custo', 'Banco'])
    fomulario.tabelaLancamentos.resizeColumnsToContents()
    fomulario.tabelaLancamentos.resizeRowsToContents()
    fomulario.tabelaLancamentos.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
    fomulario.tabelaLancamentos.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
    fomulario.tabelaLancamentos.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)

    fomulario.tabelaLancamentos.cellClicked.connect(carregar_dados_listagem)
    
    
    # Here you would typically fetch data from the database and populate the table 

def form_add_credor():
    frm_add_credor.show()

def consultar_credor():
    try:
        cnpj = str(frm_add_credor.txtCnpj.text())
        api = f"https://open.cnpja.com/office/{cnpj}"
        dados = requests.get(api).json()
        
        frm_add_credor.txtRazao.setText(dados["company"]["name"])
        frm_add_credor.txtEndereco.setText(dados["address"]["street"])
        frm_add_credor.txtNumero.setText(dados["address"]["number"])
        frm_add_credor.txtBairro.setText(dados["address"]["district"])
        frm_add_credor.txtCidade.setText(dados["address"]["city"])
        frm_add_credor.txtEstado.setText(dados["address"]["state"])

    except Exception as e:
        msg_warning(f"Erro ao consultar credor: {e}") 

def lancar_credor():
    try:
        razao = frm_add_credor.txtRazao.text()
        endereco = frm_add_credor.txtEndereco.text()
        numero = frm_add_credor.txtNumero.text()
        bairro = frm_add_credor.txtBairro.text()
        cidade = frm_add_credor.txtCidade.text()
        uf = frm_add_credor.txtEstado.text()
        cnpj = frm_add_credor.txtCnpj.text()    

        if not cnpj: 
            msg_warning("CNPJ não pode ser vazio.")
            return 
        if not razao:
            msg_warning("Razão social não pode ser vazia.")
            return
        if not endereco:
            msg_warning("Endereço não pode ser vazio.")
            return
        if not numero:
            msg_warning("Número não pode ser vazio.")
            return
        if not bairro:
            msg_warning("Bairro não pode ser vazio.")
            return
        if not cidade:
            msg_warning("Cidade não pode ser vazia.")
            return
        if not uf:
            msg_warning("UF não pode ser vazio.")
            return  
        
        criar_credor(razao, endereco, numero, bairro, cidade, uf, cnpj)

        frm_add_credor.txtRazao.clear()
        frm_add_credor.txtEndereco.clear()
        frm_add_credor.txtNumero.clear()
        frm_add_credor.txtBairro.clear()
        frm_add_credor.txtCidade.clear()
        frm_add_credor.txtEstado.clear()
        frm_add_credor.txtCnpj.clear()
        msg_info("Credor cadastrado com sucesso!")
    except Exception as e:
        msg_warning(f"Erro ao cadastrar credor: {e}")

def open_form_classificacao():
    frm_classificacao.show()

def salvar_classificacao():
    try:
        if not frm_classificacao.txtClassificacao.text():
            msg_warning("Classificação não pode ser vazia.")
            return
        classificacao = frm_classificacao.txtClassificacao.text()
        criar_classificacao(classificacao)
        frm_classificacao.txtClassificacao.clear()
        msg_info("Classificação cadastrada com sucesso!")
    except Exception as e:
        msg_warning(f"Erro ao cadastrar classificação: {e}")

def open_form_centro_custo():
    frm_centro_custo.show()

def salvar_centro_custo():
    try:
        if not frm_centro_custo.txtCentro.text():
            msg_warning("Centro de custo não pode ser vazio.")
            return
        centro_de_custo = frm_centro_custo.txtCentro.text()
        # Assuming you have a function to create a centro de custo in your db module
        criar_centro_de_custo(centro_de_custo)  # You need to implement this function in db.py
        frm_centro_custo.txtCentro.clear()
        msg_info("Centro de custo cadastrado com sucesso!")
    except Exception as e:
        msg_warning(f"Erro ao cadastrar centro de custo: {e}")

def gerar_planilha():
    try:
        mes = frm_listar_lancamentos.txtPesquisaMes.currentText()
        ano = frm_listar_lancamentos.txtPesquisaAno.currentText()
        dados = selecionar_compras_mes_ano(mes, ano)
       
        if not dados:
            msg_warning("Nenhum dado encontrado para o mês e ano selecionados.")
            return
        
        df = pd.DataFrame(dados, columns=['ID', 'DATA_DA_COMPRA', 'DATA_DO_VENCIMENTO', 'CREDOR', 'PARCELAS', 'VALOR', 'CLASSIFICACAO', 'CENTRO_DE_CUSTO', 'BANCO'])
        
        caminho = QFileDialog.getSaveFileName(
            None, 
            "Salvar Planilha", 
            "compras.xlsx", 
            "Excel Files (*.xlsx)"
        )[0]

        if caminho:
            df.to_excel(caminho, index=False)
            msg_info(f"Dados exportados com sucesso!")
        else:
            msg_warning("Operação de salvar cancelada.")   

    except Exception as e:
        msg_warning(f"Erro ao gerar planilha: {e}")


def consultar_lancamento_mes_ano():
    try:
        mes = frm_listar_lancamentos.txtPesquisaMes.currentText()
        ano = frm_listar_lancamentos.txtPesquisaAno.currentText()  
        dados = selecionar_compras_mes_ano(mes, ano)
        
        frm_listar_lancamentos.txtPesquisaAno.addItems(anos)
        frm_listar_lancamentos.tabelaLancamentos.setRowCount(len(dados))
        frm_listar_lancamentos.tabelaLancamentos.setColumnCount(9)

        for linha in range(len(dados)):
            for coluna in range(0, 9):
                frm_listar_lancamentos.tabelaLancamentos.setItem(linha, coluna, QtWidgets.QTableWidgetItem(str(dados[linha][coluna])))
            
        frm_listar_lancamentos.tabelaLancamentos.setHorizontalHeaderLabels(['ID', 'Data do Lançamento', 'Data do Vencimento', 'Credor', 'Parcelas', 'Valor', 'Classificação', 'Centro de Custo', 'Banco'])
        frm_listar_lancamentos.tabelaLancamentos.resizeColumnsToContents()
        frm_listar_lancamentos.tabelaLancamentos.resizeRowsToContents()
        frm_listar_lancamentos.tabelaLancamentos.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        frm_listar_lancamentos.tabelaLancamentos.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        frm_listar_lancamentos.tabelaLancamentos.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        frm_listar_lancamentos.lblValor.setText(f"R$ {somar_valores():.2f}")
    except Exception as e:
        msg_warning(f"Erro ao consultar lançamentos: {e}")

def carregar_dados_listagem():
    frm_editar_lancamentos.show()

    row = frm_listar_lancamentos.tabelaLancamentos.currentRow()
    if row >= 0:
        id = frm_listar_lancamentos.tabelaLancamentos.item(row, 0).text()
        data_lancamento = frm_listar_lancamentos.tabelaLancamentos.item(row, 1).text()
        data_vencimento = frm_listar_lancamentos.tabelaLancamentos.item(row, 2).text()
        credor = frm_listar_lancamentos.tabelaLancamentos.item(row, 3).text()
        parcelas = frm_listar_lancamentos.tabelaLancamentos.item(row, 4).text()
        valor = frm_listar_lancamentos.tabelaLancamentos.item(row, 5).text()
        classificacao = frm_listar_lancamentos.tabelaLancamentos.item(row, 6).text()
        centro_custo = frm_listar_lancamentos.tabelaLancamentos.item(row, 7).text()
        banco = frm_listar_lancamentos.tabelaLancamentos.item(row, 8).text()

        frm_editar_lancamentos.txtValorParcela.setText(valor)
        frm_editar_lancamentos.txtParcelas.setText(parcelas)
        frm_editar_lancamentos.txtBanco.setText(banco)
        frm_editar_lancamentos.txtCredor.setText(credor)
        frm_editar_lancamentos.txtClassificacao.setText(classificacao)
        frm_editar_lancamentos.txtCentro.setText(centro_custo)
        frm_editar_lancamentos.txtDataVencimento.setText(data_vencimento)

def open_formulario_editar_lancamentos():
    frm_editar_lancamentos.show()

def salvar_dados_fatura():
    try:
        data_vencimento = frm_editar_lancamentos.txtDataVencimento.text()
        parcela = frm_editar_lancamentos.txtParcelas.text() 
        valor_parcela = frm_editar_lancamentos.txtValorParcela.text()
        banco = frm_editar_lancamentos.txtBanco.text()
        credor = frm_editar_lancamentos.txtCredor.text()
        classificacao = frm_editar_lancamentos.txtClassificacao.text()
        centro_de_custo = frm_editar_lancamentos.txtCentro.text()
        if not data_vencimento or not parcela or not valor_parcela or not banco or not credor or not classificacao or not centro_de_custo:
            msg_warning("Todos os campos devem ser preenchidos.")
            return
        criar_fatura(data_vencimento, parcela, valor_parcela, banco, credor, classificacao, centro_de_custo)
        msg_info("Dados da fatura salvos com sucesso!")
    except Exception as e:
        msg_warning(f"Erro ao salvar dados da fatura: {e}")

def open_nota_debito():
    frm_nota_debito.show()



app = QtWidgets.QApplication([])
frm_listar_lancamentos = uic.loadUi("listar_lancamentos.ui")
frm_lancar_ars = uic.loadUi("frm_lancar_ars.ui")
frm_add_credor = uic.loadUi("frm_add_credor.ui")
frm_classificacao = uic.loadUi("frm_add_classificacao.ui")
frm_centro_custo = uic.loadUi("frm_add_centro.ui")
frm_editar_lancamentos = uic.loadUi("frm_editar_lancamento.ui")
frm_pricipal = uic.loadUi("frm_principal.ui")
frm_nota_debito = uic.loadUi("frm_nota_debito.ui")
# frm_listar_lancamentos.show()
frm_pricipal.showMaximized()

# menu principal
frm_pricipal.btnChamaFormAdd.triggered.connect(open_form_listar_lancamentos)    
frm_pricipal.btnAddCliente.triggered.connect(form_add_credor)    
frm_pricipal.btnCriarNota.triggered.connect(open_nota_debito)    

listar_lancamentos(frm_listar_lancamentos)

# menu
frm_listar_lancamentos.btnLancarAr.triggered.connect(frm_lancar_ar)
frm_listar_lancamentos.btnLancarCredor.triggered.connect(form_add_credor)
frm_listar_lancamentos.btnClassificacao.triggered.connect(open_form_classificacao)
frm_listar_lancamentos.btnCentroCusto.triggered.connect(open_form_centro_custo)
frm_listar_lancamentos.btnPesquisar.clicked.connect(consultar_lancamento_mes_ano)
frm_listar_lancamentos.btnResetarConsulta.clicked.connect(lambda: listar_lancamentos(frm_listar_lancamentos))
frm_listar_lancamentos.btnAddAr.clicked.connect(frm_lancar_ar)
frm_listar_lancamentos.btnAddCredor.clicked.connect(form_add_credor)
frm_listar_lancamentos.btnAddClassificacao.clicked.connect(open_form_classificacao)
frm_listar_lancamentos.btnAddCentroCusto.clicked.connect(open_form_centro_custo)
frm_listar_lancamentos.btnCriarPlanilha.clicked.connect(gerar_planilha)

# botoes do formulario add credor
frm_add_credor.btnConsultar.clicked.connect(consultar_credor)
frm_add_credor.btnSalvarCredor.clicked.connect(lancar_credor)

# botoes do formulario de lancar AR
frm_lancar_ars.btnSalvar.clicked.connect(salvar_parcelas)

# botao salvar classificacao
frm_classificacao.btnSalvarClassificacao.clicked.connect(salvar_classificacao)

# botao salvar centro de custo
frm_centro_custo.btnSalvar.clicked.connect(salvar_centro_custo)

# botoes do formulario editar lancamentos
frm_editar_lancamentos.btnSalvar.clicked.connect(salvar_dados_fatura)


app.exec()
  # This will print the value entered in the txtValor field