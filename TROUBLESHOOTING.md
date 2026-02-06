# TROUBLESHOOTING - Solução de Problemas Comuns

## Índice
1. [Problemas de Instalação](#problemas-de-instalação)
2. [Problemas do Banco de Dados](#problemas-do-banco-de-dados)
3. [Problemas de Servidor](#problemas-de-servidor)
4. [Problemas de Login](#problemas-de-login)
5. [Erros de Importação](#erros-de-importação)
6. [Problemas de Performance](#problemas-de-performance)

---

## Problemas de Instalação

### Erro: "Python não encontrado"
**Solução:**
1. Instale Python 3.8+ de https://python.org
2. Certifique-se de marcar "Add Python to PATH" durante instalação
3. Reinicie o terminal/CMD
4. Verifique: `python --version`

### Erro: "ModuleNotFoundError: No module named 'django'"
**Solução:**
```bash
# Ativar ambiente virtual
Windows: venv\Scripts\activate
Linux/Mac: source venv/bin/activate

# Reinstalar dependências
pip install --upgrade -r requirements.txt
```

### Erro: "pip não é reconhecido"
**Solução:**
```bash
# Use Python -m
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### Erro: "Ambiente virtual não funciona"
**Solução:**
```bash
# Delete e recrie o ambiente
rmdir venv  (Windows)
rm -rf venv (Linux)

python -m venv venv
venv\Scripts\activate  (Windows)
source venv/bin/activate  (Linux)

pip install -r requirements.txt
```

---

## Problemas do Banco de Dados

### Erro: "table factoring_app_cliente does not exist"
**Causa:** Migrations não foram executadas
**Solução:**
```bash
python manage.py migrate
python manage.py makemigrations
python manage.py migrate
```

### Erro: "database is locked"
**Causa:** Múltiplas instâncias acessando SQLite
**Solução:**
```bash
# Feche todos os servidores Django
# Exclua o arquivo de lock
rm db.sqlite3-journal  (Linux)
del db.sqlite3-journal  (Windows)

# Recrie o banco
python manage.py migrate
```

### Erro: "Column does not exist"
**Causa:** Schema desatualizado
**Solução:**
```bash
# Criar nova migration
python manage.py makemigrations factoring_app

# Aplicar
python manage.py migrate
```

### Banco de dados corrompido
**Solução extrema:**
```bash
# Backup do banco antigo
cp db.sqlite3 db.sqlite3.backup  (Linux)
copy db.sqlite3 db.sqlite3.backup  (Windows)

# Remover banco
rm db.sqlite3  (Linux)
del db.sqlite3  (Windows)

# Recriar do zero
python manage.py migrate
python manage.py createsuperuser
python manage.py shell < setup_dados_exemplo.py
```

---

## Problemas de Servidor

### Erro: "Port 8000 already in use"
**Causa:** Outro processo usando a porta 8000
**Soluções:**

Opção 1 - Usar outra porta:
```bash
python manage.py runserver 8080
```

Opção 2 - Liberar a porta (Windows):
```bash
# Encontrar processo
netstat -ano | findstr :8000

# Encerrar processo (trocar PID pelo número)
taskkill /PID NUMERO /F
```

Opção 3 - Liberar a porta (Linux/Mac):
```bash
# Encontrar processo
lsof -i :8000

# Encerrar
kill -9 PID_NUMERO
```

### Erro: "ConnectionRefusedError: [Errno 111] Connection refused"
**Causa:** Servidor não está rodando
**Solução:**
```bash
# Inicie o servidor em outro terminal
python manage.py runserver
```

### Erro: "DisallowedHost: 'seu-dominio.com'"
**Causa:** Host não está em ALLOWED_HOSTS
**Solução:** Edite `factoring_project/settings.py`
```python
# Altere:
ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'seu-dominio.com']
```

---

## Problemas de Login

### "Invalid username or password" (admin/admin123)
**Solução 1 - Resetar senha:**
```bash
python manage.py changepassword admin
```

**Solução 2 - Recriar usuário:**
```bash
python manage.py shell
```
Dentro do shell:
```python
from django.contrib.auth.models import User
User.objects.filter(username='admin').delete()
User.objects.create_superuser('admin', 'admin@factoring.com', 'admin123')
exit()
```

### Página de login congela ou trava
**Causa:** Banco de dados corrompido
**Solução:**
```bash
# Verificar integridade
python manage.py shell
```
Dentro do shell:
```python
from factoring_app.models import *
print(UsuarioPermissao.objects.count())
exit()
```

### "Session expired" ao fazer login
**Causa:** Timeout de sessão ou problema de cookie
**Solução:**
1. Limpar cache/cookies do navegador
2. Tentar em modo privado/incógnito
3. Verificar horário do sistema (importante para validação)

---

## Erros de Importação

### ImportError em migrate
**Exemplo:** `from factoring_app.models import ...`

**Solução:**
```bash
# Verificar syntax dos models
python -m py_compile factoring_app/models.py

# Validar projeto
python manage.py check

# Se tiver erro, corrigir o arquivo Python
```

### "Attempted to access a database in read-only mode"
**Causa:** Permissões de arquivo
**Solução (Linux):**
```bash
chmod 644 db.sqlite3
chmod 755 .
```

### ModuleNotFoundError em imports customizados
**Solução:**
Certifique-se de que `__init__.py` existe em todas as pastas:
```bash
# Verificar estrutura
ls -la factoring_app/__init__.py
ls -la factoring_app/migrations/__init__.py
```

---

## Problemas de Performance

### Site muito lento
**Causas possíveis e soluções:**

1. **Banco de dados grande:**
```bash
python manage.py shell
```
```python
from factoring_app.models import *
print(f"Documentos: {Documento.objects.count()}")
print(f"Borderos: {Bordero.objects.count()}")
exit()
```

2. **Queries N+1:**
Edite `factoring_app/views.py` e use `select_related()` e `prefetch_related()`:
```python
# Em vez de:
borderos = Bordero.objects.all()

# Use:
borderos = Bordero.objects.select_related('cliente', 'banco')
```

3. **Muito DEBUG:**
Se `DEBUG=True`, desative em produção:
```python
# Em settings.py
DEBUG = False
```

### Uso alto de memória
**Soluções:**

1. Limpar sessões antigas:
```bash
python manage.py clearsessions
```

2. Reduzir PAGE_SIZE em settings.py:
```python
REST_FRAMEWORK = {
    'PAGE_SIZE': 10  # Reduzir de 20 para 10
}
```

### Cursor aberto/Arquivos não fechados
**Solução:**
```bash
# Reiniciar servidor
# (CTRL+C e python manage.py runserver novamente)
```

---

## Checklist de Troubleshooting

- [ ] Python está instalado e acessível?
- [ ] Ambiente virtual está ativado?
- [ ] Dependências foram instaladas?
- [ ] Migrations foram executadas?
- [ ] Banco de dados existe e é acessível?
- [ ] Superusuário foi criado?
- [ ] Porta 8000 está livre?
- [ ] Firewall está permitindo a conexão?
- [ ] Hora do sistema está correta?
- [ ] Há espaço em disco disponível?

---

## Logs e Debugging

### Ver logs mais detalhados
```bash
# Com mais informações
python manage.py runserver --verbosity=2

# Ou editar settings.py para logging mais detalhado
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'DEBUG',
    },
}
```

### Usar modo interativo
```bash
python manage.py shell
```
```python
# Testar modelos
from factoring_app.models import Cliente
clientes = Cliente.objects.all()
print(clientes)

# Testar queries
from django.db import connection
for query in connection.queries:
    print(query)
```

### Debugger (pdb)
```python
# Em qualquer view ou modelo, adicione:
import pdb; pdb.set_trace()

# Isso pausará a execução e permitirá debugar
```

---

## Problema não listado?

1. Procure no Stack Overflow: https://stackoverflow.com/
2. Consulte docs Django: https://docs.djangoproject.com/
3. Abra uma issue no GitHub (se open-source)
4. Procure em comunidades Django

---

## Contatos Úteis

- **Django Community**: https://www.djangoproject.com/
- **Stack Overflow Django**: stackoverflow.com/questions/tagged/django
- **Real Python Django**: https://realpython.com/django/
