import os
from datetime import datetime, timedelta, date
from decimal import Decimal
from fastapi import FastAPI, Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
from .db import init_db, get_conn, qmark, rows, row, dashboard, is_pg

app=FastAPI(title='Crediário Digital Web')
app.add_middleware(SessionMiddleware, secret_key=os.getenv('SECRET_KEY','troque-esta-chave'))
app.mount('/static', StaticFiles(directory='web/static'), name='static')
templates=Jinja2Templates(directory='web/templates')

@app.on_event('startup')
def startup(): init_db()

def require_login(request:Request):
    if not request.session.get('usuario'):
        return RedirectResponse('/login', status_code=303)
    return True

def money(v):
    try: return f"R$ {float(v):,.2f}".replace(',', 'X').replace('.', ',').replace('X','.')
    except: return v
templates.env.filters['money']=money

@app.get('/login', response_class=HTMLResponse)
def login_get(request:Request): return templates.TemplateResponse('login.html', {'request':request, 'erro':''})

@app.post('/login')
def login_post(request:Request, usuario:str=Form(...), senha:str=Form(...)):
    with get_conn() as c:
        cur=c.cursor(); cur.execute(qmark('SELECT * FROM usuarios WHERE usuario=%s AND senha=%s'),(usuario,senha)); u=row(cur)
    if not u: return templates.TemplateResponse('login.html', {'request':request, 'erro':'Usuário ou senha inválidos'})
    request.session['usuario']=usuario
    return RedirectResponse('/', status_code=303)

@app.get('/sair')
def sair(request:Request): request.session.clear(); return RedirectResponse('/login', status_code=303)

@app.get('/', response_class=HTMLResponse)
def home(request:Request):
    if not request.session.get('usuario'): return RedirectResponse('/login', status_code=303)
    return templates.TemplateResponse('index.html', {'request':request, 'd':dashboard()})

@app.get('/clientes', response_class=HTMLResponse)
def clientes(request:Request, q:str=''):
    if not request.session.get('usuario'): return RedirectResponse('/login', status_code=303)
    with get_conn() as c:
        cur=c.cursor(); like=f'%{q}%'
        cur.execute(qmark("SELECT * FROM clientes WHERE ativo=TRUE AND (nome ILIKE %s OR telefone ILIKE %s OR rota ILIKE %s) ORDER BY nome" if is_pg() else "SELECT * FROM clientes WHERE ativo=1 AND (nome LIKE %s OR telefone LIKE %s OR rota LIKE %s) ORDER BY nome"),(like,like,like)); lista=rows(cur)
    return templates.TemplateResponse('clientes.html', {'request':request,'clientes':lista,'q':q})

@app.post('/clientes')
def salvar_cliente(nome:str=Form(...), documento:str=Form(''), telefone:str=Form(''), endereco:str=Form(''), bairro:str=Form(''), cidade:str=Form(''), rota:str=Form('Rota 1')):
    with get_conn() as c:
        c.cursor().execute(qmark('INSERT INTO clientes(nome,documento,telefone,endereco,bairro,cidade,rota) VALUES(%s,%s,%s,%s,%s,%s,%s)'),(nome,documento,telefone,endereco,bairro,cidade,rota))
    return RedirectResponse('/clientes', status_code=303)

@app.get('/clientes/{id}/excluir')
def excluir_cliente(id:int):
    with get_conn() as c: c.cursor().execute(qmark('UPDATE clientes SET ativo=FALSE WHERE id=%s' if is_pg() else 'UPDATE clientes SET ativo=0 WHERE id=%s'),(id,))
    return RedirectResponse('/clientes', status_code=303)

@app.get('/vendas', response_class=HTMLResponse)
def vendas_get(request:Request):
    if not request.session.get('usuario'): return RedirectResponse('/login', status_code=303)
    with get_conn() as c:
        cur=c.cursor(); cur.execute('SELECT id,nome FROM clientes WHERE ativo=TRUE ORDER BY nome' if is_pg() else 'SELECT id,nome FROM clientes WHERE ativo=1 ORDER BY nome'); cs=rows(cur)
    return templates.TemplateResponse('vendas.html', {'request':request,'clientes':cs})

@app.post('/vendas')
def vendas_post(cliente_id:int=Form(...), descricao:str=Form(''), valor_total:float=Form(...), parcelas:int=Form(...), primeiro_vencimento:str=Form(...)):
    with get_conn() as c:
        cur=c.cursor()
        if is_pg():
            cur.execute('INSERT INTO vendas(cliente_id,descricao,valor_total) VALUES(%s,%s,%s) RETURNING id',(cliente_id,descricao,valor_total)); venda_id=row(cur)['id']
        else:
            cur.execute('INSERT INTO vendas(cliente_id,descricao,valor_total) VALUES(?,?,?)',(cliente_id,descricao,valor_total)); venda_id=cur.lastrowid
        base=datetime.strptime(primeiro_vencimento,'%Y-%m-%d').date(); valor=round(valor_total/parcelas,2)
        for n in range(1,parcelas+1):
            venc=base+timedelta(days=30*(n-1))
            cur.execute(qmark('INSERT INTO parcelas(venda_id,cliente_id,numero,valor,vencimento) VALUES(%s,%s,%s,%s,%s)'),(venda_id,cliente_id,n,valor,venc.isoformat()))
    return RedirectResponse('/parcelas', status_code=303)

@app.get('/parcelas', response_class=HTMLResponse)
def parcelas(request:Request, status:str='aberta', q:str=''):
    if not request.session.get('usuario'): return RedirectResponse('/login', status_code=303)
    with get_conn() as c:
        cur=c.cursor(); like=f'%{q}%'
        sql='''SELECT p.*, c.nome, c.rota FROM parcelas p JOIN clientes c ON c.id=p.cliente_id WHERE p.status=%s AND (c.nome ILIKE %s OR c.rota ILIKE %s) ORDER BY p.vencimento, c.nome''' if is_pg() else '''SELECT p.*, c.nome, c.rota FROM parcelas p JOIN clientes c ON c.id=p.cliente_id WHERE p.status=? AND (c.nome LIKE ? OR c.rota LIKE ?) ORDER BY p.vencimento, c.nome'''
        cur.execute(sql,(status,like,like)); ps=rows(cur)
    return templates.TemplateResponse('parcelas.html', {'request':request,'parcelas':ps,'status':status,'q':q})

@app.get('/parcelas/{id}/baixar')
def baixar(id:int):
    with get_conn() as c: c.cursor().execute(qmark("UPDATE parcelas SET status='paga', data_pagamento=CURRENT_DATE, valor_pago=valor WHERE id=%s"),(id,))
    return RedirectResponse('/parcelas', status_code=303)

@app.get('/parcelas/{id}/reverter')
def reverter(id:int):
    with get_conn() as c: c.cursor().execute(qmark("UPDATE parcelas SET status='aberta', data_pagamento=NULL, valor_pago=0 WHERE id=%s"),(id,))
    return RedirectResponse('/parcelas?status=paga', status_code=303)
