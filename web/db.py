import os, sqlite3
from contextlib import contextmanager
from datetime import date

DATABASE_URL=os.getenv('CREDIARIO_DATABASE_URL','').strip()
BACKEND=os.getenv('CREDIARIO_DB_BACKEND','sqlite').strip().lower()
SQLITE_PATH=os.getenv('SQLITE_PATH','crediario_web.sqlite3')

try:
    import psycopg
    from psycopg.rows import dict_row
except Exception:
    psycopg=None

def is_pg():
    return BACKEND=='postgresql' and DATABASE_URL and psycopg is not None

@contextmanager
def get_conn():
    if is_pg():
        conn=psycopg.connect(DATABASE_URL, row_factory=dict_row)
        try:
            yield conn
            conn.commit()
        finally:
            conn.close()
    else:
        conn=sqlite3.connect(SQLITE_PATH)
        conn.row_factory=sqlite3.Row
        try:
            yield conn
            conn.commit()
        finally:
            conn.close()

def qmark(sql):
    return sql.replace('%s','?') if not is_pg() else sql

def rows(cur):
    return [dict(r) for r in cur.fetchall()]

def row(cur):
    r=cur.fetchone(); return dict(r) if r else None

def init_db():
    with get_conn() as c:
        cur=c.cursor()
        if is_pg():
            cur.execute('''CREATE TABLE IF NOT EXISTS usuarios(id SERIAL PRIMARY KEY, usuario TEXT UNIQUE NOT NULL, senha TEXT NOT NULL)''')
            cur.execute('''CREATE TABLE IF NOT EXISTS clientes(id SERIAL PRIMARY KEY, nome TEXT NOT NULL, documento TEXT, telefone TEXT, endereco TEXT, bairro TEXT, cidade TEXT, rota TEXT DEFAULT 'Rota 1', ativo BOOLEAN DEFAULT TRUE, criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
            cur.execute('''CREATE TABLE IF NOT EXISTS vendas(id SERIAL PRIMARY KEY, cliente_id INTEGER REFERENCES clientes(id), descricao TEXT, valor_total NUMERIC(12,2) NOT NULL, data_venda DATE DEFAULT CURRENT_DATE)''')
            cur.execute('''CREATE TABLE IF NOT EXISTS parcelas(id SERIAL PRIMARY KEY, venda_id INTEGER REFERENCES vendas(id), cliente_id INTEGER REFERENCES clientes(id), numero INTEGER NOT NULL, valor NUMERIC(12,2) NOT NULL, vencimento DATE NOT NULL, status TEXT DEFAULT 'aberta', data_pagamento DATE, valor_pago NUMERIC(12,2) DEFAULT 0)''')
        else:
            cur.execute('''CREATE TABLE IF NOT EXISTS usuarios(id INTEGER PRIMARY KEY AUTOINCREMENT, usuario TEXT UNIQUE NOT NULL, senha TEXT NOT NULL)''')
            cur.execute('''CREATE TABLE IF NOT EXISTS clientes(id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT NOT NULL, documento TEXT, telefone TEXT, endereco TEXT, bairro TEXT, cidade TEXT, rota TEXT DEFAULT 'Rota 1', ativo INTEGER DEFAULT 1, criado_em TEXT DEFAULT CURRENT_TIMESTAMP)''')
            cur.execute('''CREATE TABLE IF NOT EXISTS vendas(id INTEGER PRIMARY KEY AUTOINCREMENT, cliente_id INTEGER, descricao TEXT, valor_total REAL NOT NULL, data_venda TEXT DEFAULT CURRENT_DATE)''')
            cur.execute('''CREATE TABLE IF NOT EXISTS parcelas(id INTEGER PRIMARY KEY AUTOINCREMENT, venda_id INTEGER, cliente_id INTEGER, numero INTEGER NOT NULL, valor REAL NOT NULL, vencimento TEXT NOT NULL, status TEXT DEFAULT 'aberta', data_pagamento TEXT, valor_pago REAL DEFAULT 0)''')
        cur.execute(qmark('INSERT INTO usuarios(usuario, senha) SELECT %s, %s WHERE NOT EXISTS (SELECT 1 FROM usuarios WHERE usuario=%s)'),('admin','admin','admin'))

def dashboard():
    with get_conn() as c:
        cur=c.cursor()
        data={}
        cur.execute('SELECT COUNT(*) AS total FROM clientes WHERE ativo=TRUE' if is_pg() else 'SELECT COUNT(*) AS total FROM clientes WHERE ativo=1'); data['clientes']=row(cur)['total']
        cur.execute("SELECT COUNT(*) AS total FROM parcelas WHERE status='aberta'"); data['abertas']=row(cur)['total']
        cur.execute("SELECT COUNT(*) AS total FROM parcelas WHERE status='aberta' AND vencimento < CURRENT_DATE" if is_pg() else "SELECT COUNT(*) AS total FROM parcelas WHERE status='aberta' AND date(vencimento) < date('now')"); data['atrasadas']=row(cur)['total']
        cur.execute("SELECT COUNT(*) AS total FROM parcelas WHERE status='aberta' AND vencimento = CURRENT_DATE" if is_pg() else "SELECT COUNT(*) AS total FROM parcelas WHERE status='aberta' AND date(vencimento) = date('now')"); data['hoje']=row(cur)['total']
        return data
