# Crediário Digital V2.0

Aplicativo desktop para Windows feito com Python, Tkinter e SQLite.

## Funcionalidades

- Login.
- Botao com foco pode ser acionado pela tecla Enter.
- Maximizar e restaurar a janela com F12.
- Rodape no login e na interface com logo da Realtec Informatica, contato e Diego Santos.
- Rolagem das telas pela bolinha do mouse.
- Rolagem das listas de pesquisa e tabelas pela bolinha do mouse.
- Movimentacao das opcoes de pesquisa pela bolinha do mouse enquanto a lista esta aberta.
- Configuracoes para dados da empresa e logo.
- Backup manual dos dados na tela Configuracao.
- Backup automatico de seguranca ao fechar o programa.
- Restauracao de fabrica pela tela Configuracao com usuario master e senha master.
- Exibicao da logo no login e no menu principal.
- Botao para remover a logo cadastrada.
- Alteracao da senha padrao do usuario.
- Cadastro de dados para recuperacao de senha.
- Recuperacao de senha pelo login com nome completo, data de nascimento, telefone e confirmacao da nova senha.
- Recuperacao de senha por usuario master e senha master.
- Botao para restaurar a senha padrao `admin` usando usuario master e senha master.
- Cadastro e edicao de clientes.
- Pesquisa dentro do cadastro de clientes para selecionar e alterar dados.
- Pesquisa do cadastro de clientes com filtro por rota.
- Sugestoes de clientes no cadastro ao digitar a primeira letra.
- Selecao de cliente por Enter nas listas de sugestoes.
- Navegacao nas sugestoes usando setas do teclado.
- Sugestoes de clientes sem codigo/ID antes do nome.
- Grades sem coluna ID visivel.
- Cadastro de bairro e cidade do cliente.
- Cadastro da rota do cliente, de Rota 1 a Rota 5.
- Nova venda.
- Nova venda sem campo de descricao obrigatorio.
- Nova venda com pesquisa de cliente.
- Pesquisa de cliente na venda com sugestoes exibidas ao digitar a primeira letra.
- Geracao automatica de parcelas.
- Lista de vencimentos em aberto.
- Lista de vencimentos sem coluna de venda.
- Filtro de vencimentos por rota.
- Sugestoes na pesquisa de vencimentos e baixa ao digitar.
- Selecao de vencimento por Enter na lista de sugestoes.
- Baixa de pagamento.
- Pesquisa de parcelas baixadas/pagas.
- Reversao de baixa para voltar parcela ao status aberto.
- Relatorio de inadimplentes.
- Relatorio de inadimplentes + vencimentos do dia.
- Relatorio de vencimentos do dia.
- Relatorio de vencimentos do mes.
- Relatorios com documento, telefone e endereco do cliente.
- Filtro de relatorios por rota.
- Visualizacao de relatorios dentro do programa antes de imprimir.
- Impressao de relatorios em PDF apos visualizar.
- Geracao de arquivo PDF dos relatorios.
- Dados da empresa e logo no relatorio em PDF.
- PDF de relatorio configurado para folha A4 em paisagem.
- Pesquisa por cliente.
- Pesquisa por cliente com filtro por rota.
- Pesquisa por cliente com sugestoes exibidas ao digitar a primeira letra.
- Botao para limpar pesquisa de cliente.
- Pesquisa por cliente com data de baixa/pagamento no historico.
- Historico do cliente ordenado automaticamente por numero da parcela, agrupando parcela 1 de todas as vendas, depois parcela 2, e assim por diante.

## Primeiro acesso

- Usuario: `admin`
- Senha: `admin`

Troque a senha na tela Configuracoes. Para usar a recuperacao de senha pelo login,
cadastre antes os dados de recuperacao na tela Configuracoes.
Tambem existe recuperacao pela senha master: usuario master `realtec` e senha master `07596913989`.

## Como executar no Windows

1. Instale Python 3.11 ou superior em `https://www.python.org/downloads/windows/`.
2. Durante a instalacao, marque `Add python.exe to PATH`.
3. Abra o PowerShell na pasta do projeto.
4. Execute:

```powershell
.\scripts\executar.ps1
```

Tambem pode dar duplo clique em `executar.bat`.

O banco SQLite sera criado automaticamente no primeiro uso.

## Backup

Na tela Configuracao, use `Fazer backup agora` para criar uma copia do banco.
Por padrao, o programa tambem cria um backup automatico ao fechar.
Os arquivos sao salvos na pasta:

```text
Backup
```

## Banco de dados

Por padrao, o programa salva o banco em:

```text
%LOCALAPPDATA%\CrediarioSimples\crediario.sqlite3
```

Isso evita perder dados quando o programa for instalado em `Arquivos de Programas`.
O nome interno da pasta de dados foi mantido como `CrediarioSimples` para preservar cadastros ja existentes.

## Gerar executavel sem custo

Execute:

```powershell
.\scripts\gerar_executavel.ps1
```

Tambem pode dar duplo clique em `gerar_executavel.bat`.

O executavel sera gerado em:

```text
dist\CrediarioDigital\CrediarioDigital.exe
```

## Gerar instalador sem custo

1. Gere primeiro o executavel com `.\scripts\gerar_executavel.ps1`.
2. Execute:

```powershell
.\scripts\gerar_instalador.ps1
```

Tambem pode dar duplo clique em `gerar_instalador.bat`.

O instalador sera criado em:

```text
dist\installer\Instalador-CrediarioDigital-V2.0.exe
```

O instalador nao depende de licenca paga. Ele usa recursos gratuitos do Windows/.NET para criar o pacote.
Para instalar, informe a senha:

```text
admin
```

Ao instalar, o programa sera colocado em:

```text
C:\CrediarioDigital
```

A pasta de backup sera criada em:

```text
C:\CrediarioDigital\Backup
```

Durante a instalacao, o assistente agora oferece:

- `Servidor`: instala a maquina principal, baixa e instala o PostgreSQL automaticamente, cria a base principal e grava a configuracao.
- `Maquina do usuario`: instala a estacao e grava a conexao apontando para o servidor da rede.

Ao finalizar, o instalador salva:

```text
C:\CrediarioDigital\data\database.json
C:\CrediarioDigital\data\instalacao.txt
```

No modo `Servidor`, o instalador tambem mostra e salva o endereco que deve ser usado nas outras estacoes.
Se houver internet no momento da instalacao, ele baixa o instalador oficial do PostgreSQL para Windows e executa a instalacao silenciosa.

## Estrutura

```text
main.py
executar.bat
gerar_executavel.bat
gerar_instalador.bat
src\crediario_app\app.py
src\crediario_app\database.py
src\crediario_app\repository.py
scripts\executar.ps1
scripts\gerar_executavel.ps1
scripts\gerar_instalador.ps1
scripts\preparar_banco.ps1
installer\CrediarioDigital.iss
requirements.txt
```

## Multiusuario em rede local

O projeto agora pode trabalhar de dois jeitos:

- `SQLite` local, para uso simples em um unico computador.
- `PostgreSQL` em rede local, para varias maquinas acessando o mesmo banco ao mesmo tempo.

O arquivo de configuracao principal fica em:

```text
data\database.json
```

Exemplo para PostgreSQL:

```json
{
  "backend": "postgresql",
  "host": "192.168.0.10",
  "port": 5432,
  "database": "crediario_digital",
  "user": "crediario_app",
  "password": "troque-esta-senha",
  "sslmode": "prefer"
}
```

Guia completo de implantacao:

```text
docs\implantacao_rede_local_postgresql.md
```

## Observacoes

Esta versao continua funcionando localmente em um computador Windows, mas agora tambem pode ser implantada em rede local usando PostgreSQL como banco central.
