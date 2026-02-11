# Sistema de Factoring - Django

Projeto Django para gerenciamento completo de sistema de factoring, com funcionalidades de cadastro de clientes, borderos, documentos e relatórios.

## Estrutura do Projeto

```
factoring_django/
├── manage.py                        # Arquivo de gerenciamento Django
├── requirements.txt                 # Dependências Python
├── db.sqlite3                       # Banco de dados SQLite
├── factoring_project/               # Pasta do projeto
│   ├── __init__.py
│   ├── settings.py                 # Configurações do Django
│   ├── urls.py                     # URLs principais
│   ├── wsgi.py                     # WSGI
│   ├── templates/
│   │   ├── base.html               # Template base
│   │   └── factoring_app/          # Templates da aplicação
│   └── static/                     # Arquivos estáticos (CSS, JS)
├── factoring_app/                   # Aplicação principal
│   ├── models.py                   # Modelos do banco de dados
│   ├── views.py                    # Views/Controladores
│   ├── urls.py                     # URLs da aplicação
│   ├── admin.py                    # Admin customizado
│   ├── apps.py                     # Configuração da app
│   └── migrations/                 # Migrations do banco de dados
└── README.md
```

## Instalação

### Pré-requisitos

- Python 3.8+
- pip (gerenciador de pacotes Python)

### Passo a Passo

1. **Criar ambiente virtual:**
```bash
cd D:\Jose Celso\Downloads\FACTORING\factoring_django

# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

2. **Instalar dependências:**
```bash
pip install -r requirements.txt
```

3. **Executar migrations:**
```bash
python manage.py migrate
```

4. **Criar superusuário (admin):**
```bash
python manage.py createsuperuser
```

5. **Iniciar servidor:**
```bash
python manage.py runserver
```

Acesse em: http://127.0.0.1:8000

## Funcionalidades Implementadas

### 1. Autenticação
- Login/Logout de usuários
- Sistema de permissões por usuário
- Níveis de acesso (Admin, Gerente, Operador, Visualizador)

### 2. Gestão de Clientes
- CRUD completo de clientes
- Filtros por nome, CPF/CNPJ, status
- Visualização de detalhes e histórico

### 3. Gestão de Borderos
- Criar e gerenciar borderos de cobrança
- Status de processamento (Novo, Processando, Enviado, Concluído, Cancelado)
- Listagem e detalhes de cada bordero

### 4. Gestão de Documentos
- Cadastro de documentos/títulos
- Associação com borderos e sacados
- Controle de vencimentos
- Desconto e valor líquido
- Status de pagamento (Pendente, Pago, Cancelado, Devolvido)

### 5. Gestão Bancária
- Cadastro de bancos
- Gerenciamento de agências
- Controle de contas bancárias

### 6. Relatórios
- **Pendências**: Documentos em aberto com identificação de vencidos
- **Fluxo de Caixa**: Entrada de pagamentos por período
- **Clientes**: Resumo de todos os clientes com limite e saldo

### 7. Configurações
- Sistema de parâmetros gerais
- Gestão de feriados
- Tipos de documentos
- Ocorrências de cobrança

### 8. Auditoria
- Log completo de operações
- Rastreamento de usuário que realizou ação
- Registro de tipo de operação (criar, atualizar, deletar, consultar)

## Modelos Principal

### Cliente
- Código, Nome, Tipo (PF/PJ), CPF/CNPJ
- Contato e endereço
- Limite de crédito e saldo devedor

### Bordero
- Número, Cliente, Banco
- Status e datas
- Quantidade e valor total

### Documento
- Número, Tipo, Sacado
- Datas de emissão e vencimento
- Valor, taxa de desconto, valor líquido
- Status (Pendente, Pago, etc)

### Pagamento
- Associado ao documento
- Tipo (Boleto, Cheque, Transferência, etc)
- Valor e data

### Usuário e Permissões
- Integrado com Django Auth
- Tipos: Admin, Gerente, Operador, Visualizador
- Permissões granulares

## Admin Django

Acesse o painel admin em: http://127.0.0.1:8000/admin

Utilize as credenciais do superusuário criado.

Funcionalidades:
- Gerenciar todos os modelos
- Adicionar/Editar/Deletar registros
- Busca e filtros avançados

## URLs Disponíveis

- `/` - Login
- `/dashboard/` - Dashboard principal
- `/clientes/` - Lista de clientes
- `/clientes/criar/` - Criar novo cliente
- `/clientes/<id>/` - Detalhes do cliente
- `/borderos/` - Lista de borderos
- `/borderos/<id>/` - Detalhes do bordero
- `/documentos/` - Lista de documentos
- `/documentos/<id>/` - Detalhes do documento
- `/bancos/` - Lista de bancos
- `/bancos/<id>/` - Detalhes do banco
- `/relatorios/pendencias/` - Relatório de pendências
- `/relatorios/fluxo-caixa/` - Relatório de fluxo de caixa
- `/relatorios/clientes/` - Relatório de clientes
- `/admin/` - Painel administrativo
- `/logout/` - Logout

## Comando Úteis Django

```bash
# Executar migrations
python manage.py migrate

# Criar migration para mudanças em models
python manage.py makemigrations

# Ver status das migrations
python manage.py showmigrations

# Shell interativo Django
python manage.py shell

# Executar testes
python manage.py test

# Limpeza de dados
python manage.py flush

# Collectar static files (produção)
python manage.py collectstatic
```

## Próximas Melhorias

1. API REST com Django REST Framework
2. Sistema de emails automáticos
3. Integração com bancos (API)
4. Exportação de relatórios (PDF, Excel)
5. Dashboard com gráficos
6. Mobile responsive melhorado
7. Testes automatizados
8. Autenticação com token JWT
9. Agendamento de tarefas (Celery)
10. Notificações em tempo real

## Configurações de Produção

Para usar em produção:

1. Alterar `DEBUG = False` em `settings.py`
2. Definir `SECRET_KEY` em variável de ambiente
3. Configurar `ALLOWED_HOSTS`
4. Usar banco de dados PostgreSQL ou MySQL
5. Usar servidor WSGI (Gunicorn, uWSGI)
6. Configurar HTTPS
7. Definir STATIC_ROOT e MEDIA_ROOT

## Suporte

Para dúvidas ou problemas, consulte a documentação Django:
- https://docs.djangoproject.com/
- https://www.djangoproject.com/
