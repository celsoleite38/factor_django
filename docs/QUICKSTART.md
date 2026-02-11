# GUIA RÁPIDO - Início em 5 Minutos

## Opção 1: Windows (Mais Rápido)

Abra o PowerShell ou CMD na pasta `factoring_django` e execute:

```bash
setup.bat
```

Pronto! O servidor será iniciado automaticamente. Acesse:
- **Sistema**: http://127.0.0.1:8000
- **Admin**: http://127.0.0.1:8000/admin
- **Credenciais**: admin / admin123

---

## Opção 2: Linux / Mac

Abra o terminal na pasta `factoring_django` e execute:

```bash
chmod +x setup.sh
./setup.sh
```

---

## Opção 3: Manual (Passo a Passo)

### 1. Criar Ambiente Virtual
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 2. Instalar Dependências
```bash
pip install -r requirements.txt
```

### 3. Preparar Banco de Dados
```bash
python manage.py migrate
```

### 4. Criar Admin (Opcional)
```bash
python manage.py createsuperuser
```
Se não quiser createuser interativo, use:
```bash
python manage.py shell
```
Dentro do shell:
```python
from django.contrib.auth.models import User
User.objects.create_superuser('admin', 'admin@factoring.com', 'admin123')
```

### 5. Carregar Dados de Exemplo (Opcional)
```bash
python manage.py shell < setup_dados_exemplo.py
```

### 6. Iniciar Servidor
```bash
python manage.py runserver
```

---

## Primeiros Passos no Sistema

1. **Acesse** http://127.0.0.1:8000
2. **Login** com: admin / admin123
3. **Explore**:
   - Dashboard - visão geral do sistema
   - Clientes - cadastre seus clientes
   - Borderos - crie seus borderos de cobrança
   - Relatórios - acompanhe os dados

---

## Primeiros Cadastros Recomendados

### 1. Bancos
- Menu Admin → Bancos
- Adicione os bancos que sua empresa usa

### 2. Agências
- Menu Admin → Agências
- Adicione as agências de seus bancos

### 3. Contas Bancárias
- Menu Admin → Contas Bancárias
- Adicione suas contas

### 4. Clientes
- Clientes → Novo Cliente
- Ou use o formulário manual

### 5. Tipos de Documentos
- Menu Admin → Tipos de Documentos
- Dupla, Nota Promissória, etc

### 6. Ocorrências
- Menu Admin → Ocorrências
- Pagamento, Devolução, Protesto, etc

---

## Comandos Úteis

```bash
# Ver status do banco de dados
python manage.py showmigrations

# Criar migration para mudanças em models
python manage.py makemigrations

# Aplicar migrations
python manage.py migrate

# Criar novo superusuário
python manage.py createsuperuser

# Limpar todos os dados (CUIDADO!)
python manage.py flush

# Fazer shell interativo
python manage.py shell

# Coletar static files (produção)
python manage.py collectstatic

# Executar servidor em porta diferente
python manage.py runserver 8080

# Executar servidor escutando em todas as interfaces
python manage.py runserver 0.0.0.0:8000
```

---

## Solução de Problemas

### "ModuleNotFoundError: No module named 'django'"
- Certifique-se de ter ativado o ambiente virtual
- Execute `pip install -r requirements.txt`

### "Port 8000 already in use"
```bash
python manage.py runserver 8080
```

### Banco de dados corrompido
```bash
# Remova o banco antigo
rm db.sqlite3

# Recrie do zero
python manage.py migrate
```

### Esquecer senha admin
```bash
python manage.py changepassword admin
```

---

## Estrutura de Pastas

```
factoring_django/
├── manage.py                  # Gerenciamento Django
├── requirements.txt          # Dependências
├── db.sqlite3               # Banco de dados
├── setup.bat / setup.sh     # Scripts de inicialização
├── README.md                # Documentação completa
├── MIGRACAO_VB6.md         # Guia de migração
├── factoring_project/       # Projeto Django
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── templates/           # Templates HTML
├── factoring_app/           # Aplicação principal
│   ├── models.py           # Modelos do banco
│   ├── views.py            # Lógica das páginas
│   ├── urls.py             # Rotas
│   ├── admin.py            # Painel admin
│   └── migrations/         # Histórico de mudanças
├── static/                 # CSS, JS, imagens
└── media/                  # Arquivos de usuários
```

---

## Próximos Passos

1. **Customize**: Edite `factoring_project/settings.py` se necessário
2. **Modelos**: Adicione campos em `factoring_app/models.py` se precisar
3. **Views**: Edite `factoring_app/views.py` para mais funcionalidades
4. **Templates**: Customize os HTML em `factoring_project/templates`
5. **Deploy**: Quando pronto, suba em um servidor (Heroku, AWS, etc)

---

## Precisa de Ajuda?

- Documentação Django: https://docs.djangoproject.com/
- Python Docs: https://docs.python.org/
- Django Community: https://www.djangoproject.com/

Boa diversão! 🚀
