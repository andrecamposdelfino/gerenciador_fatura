import sqlite3

connection = sqlite3.connect("db_compras.db")
cursor = connection.cursor()

def create_table():
    cursor.execute('''

    CREATE TABLE IF NOT EXISTS compras (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        data_do_lancamento TEXT NOT NULL,
        data_do_vencimento TEXT NOT NULL,
        CREDOR TEXT NOT NULL,
        PARCELAS TEXT NOT NULL,
        VALOR REAL NOT NULL,
        CLASSIFICACAO TEXT NOT NULL,
        CENTRO_DE_CUSTO TEXT NOT NULL
    )
    ''')
    connection.commit()

def criar(data_do_lancamento, data_do_vencimento, credor, parcelas, valor, classificacao, centro_de_custo, banco):
    cursor.execute('''
    INSERT INTO compras (data_do_lancamento, data_do_vencimento, CREDOR, PARCELAS, VALOR, CLASSIFICACAO, CENTRO_DE_CUSTO, BANCO)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (data_do_lancamento, data_do_vencimento, credor, parcelas, valor, classificacao, centro_de_custo, banco))
    connection.commit()

def somar_valores():
    cursor.execute('SELECT SUM(VALOR) FROM compras')
    total = cursor.fetchone()[0]
    return total if total is not None else 0



def selecionar_todas_as_compras():
    cursor.execute('SELECT * FROM compras')
    dados = cursor.fetchall()
    return dados

def selecionar_compras_mes_ano(mes, ano):
    # mes e ano devem ser strings, ex: mes="09", ano="2025"
    filtro = f"%/{mes}/{ano}"
    cursor.execute('SELECT * FROM compras WHERE data_do_vencimento LIKE ?', (filtro,))
    dados = cursor.fetchall()
    return dados

def deletar_dados_compras():
    cursor.execute('DELETE FROM compras')
    connection.commit()

def criar_credor(razao, endereco, numero, bairro, cidade, uf, cnpj):
    cursor.execute('''
    INSERT INTO credor (razao, endereco, numero, bairro, cidade, uf, cnpj)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (razao, endereco, numero, bairro, cidade, uf, cnpj))
    connection.commit()

def listar_credor():
    cursor.execute('SELECT * FROM credor')
    dados = cursor.fetchall()
    return dados

def criar_classificacao(classificacao):
    cursor.execute('''
    INSERT INTO classificacao (classificacao)
    VALUES (?)
    ''', (classificacao,))
    connection.commit()

def listar_classificacao():
    cursor.execute('SELECT * FROM classificacao')
    dados = cursor.fetchall()
    return dados

def criar_centro_de_custo(centro_de_custo):
    cursor.execute('''
    INSERT INTO centro_de_custo (centro_de_custo)
    VALUES (?)
    ''', (centro_de_custo,))
    connection.commit()

def listar_centro_de_custo():
    cursor.execute('SELECT * FROM centro_de_custo')
    dados = cursor.fetchall()
    return dados

def criar_fatura(data_vencimento, parcela, valor_parcela, banco, credor, classificacao, centro_de_custo):
    cursor.execute('''
    INSERT INTO fatura (data_vencimento, parcela, valor_parcela, banco, credor, classificacao, centro_de_custo)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (data_vencimento, parcela, valor_parcela, banco, credor, classificacao, centro_de_custo))
    connection.commit()

def selecionar_fatura():
    cursor.execute('SELECT * FROM fatura')
    dados = cursor.fetchall()
    return dados

def criar_nota(empresa, endereco_empresa, numero_empresa, bairro_empresa, cidade_empresa, estado_empresa, cnpj_empresa, cliente, endereco_cliente, numero_cliente, bairro_cliente, cidade_cliente, estado_cliente, cnpj_cliente, numero_nota, vencimento, valor_total, periodo1, periodo2, servico, qtde, unidade, valor_unitario, valor_total_nota, valor_por_extenso, dados_bancarios, observacao):
    cursor.execute('''
    INSERT INTO notas (empresa, endereco_empresa, numero_empresa, bairro_empresa, cidade_empresa, estado_empresa, cnpj_empresa, cliente, endereco_cliente, numero_cliente, bairro_cliente, cidade_cliente, estado_cliente, cnpj_cliente, numero_nota, vencimento, valor_total, periodo1, periodo2, servico, qtde, unidade, valor_unitario, valor_total_nota, valor_por_extenso, dados_bancarios, observacao)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (empresa, endereco_empresa, numero_empresa, bairro_empresa, cidade_empresa, estado_empresa, cnpj_empresa, cliente, endereco_cliente, numero_cliente, bairro_cliente, cidade_cliente, estado_cliente, cnpj_cliente, numero_nota, vencimento, valor_total, periodo1, periodo2, servico, qtde, unidade, valor_unitario, valor_total_nota, valor_por_extenso, dados_bancarios, observacao))
    connection.commit()

