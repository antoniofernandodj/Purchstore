import sqlite3
from uuid import uuid4

# DATABASE = 'purchstore/database/compras.sqlite3'
DATABASE = 'compras.sqlite3'


def criar_banco_de_dados(db_name=DATABASE):
    conn = sqlite3.connect(db_name)
    try:
        cursor = conn.cursor()

        cursor.execute("PRAGMA foreign_keys = ON;")
        conn.commit()

        sql1 = '''
            CREATE TABLE IF NOT EXISTS compra (
                id TEXT PRIMARY KEY,
                mercado TEXT,
                emissao TEXT,
                emissao_datetime DATETIME,
                serie TEXT,
                numero TEXT,
                total REAL,
                n_itens INTEGER
            )
        '''

        cursor.execute(sql1)
        conn.commit()

        sql2 = '''
            CREATE TABLE IF NOT EXISTS item_compra (
                id TEXT PRIMARY KEY,
                compra_id TEXT,
                codigo TEXT,
                name TEXT,
                quantidade REAL,
                unidade TEXT,
                valor_unitario REAL,
                valor_total REAL,
                FOREIGN KEY (compra_id) REFERENCES compra (id)
            )
        '''

        cursor.execute(sql2)
        conn.commit()

    except sqlite3.OperationalError as e:
        print(f"Erro de operação SQL: {e}")
    finally:
        conn.close()


def inserir_itens_compra(itens_compra, compra_id, db_name=DATABASE):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    for item in itens_compra:
        cursor.execute('''
            INSERT INTO item_compra (
                id,
                codigo,
                compra_id,
                name,
                quantidade,
                unidade,
                valor_unitario,
                valor_total
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            str(uuid4()),
            item.codigo,
            compra_id,
            item.name,
            item.quantidade,
            item.unidade,
            item.valor_unitario,
            item.valor_total
        ))

    conn.commit()
    conn.close()


def inserir_compra(compra, db_name=DATABASE):

    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    cursor.execute('''
        SELECT id FROM compra WHERE emissao_datetime = ?
    ''', (compra.emissao_datetime,))

    existing_compra = cursor.fetchone()

    if not existing_compra:
        compra.id = str(uuid4())

        cursor.execute('''
            INSERT INTO compra (
                id,
                mercado,
                emissao,
                emissao_datetime,
                serie,
                numero,
                total,
                n_itens
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            compra.id,
            compra.mercado,
            compra.emissao,
            compra.emissao_datetime,
            compra.serie,
            compra.numero,
            compra.total,
            compra.n_itens
        ))

        conn.commit()
        conn.close()

    else:
        cursor.close()
        conn.close()

    if compra.id:
        inserir_itens_compra(compra.itens, compra.id)
        file_path = f"dump/{compra.get_filename()}.csv"
        compra.export_items_to_csv(file_path)
