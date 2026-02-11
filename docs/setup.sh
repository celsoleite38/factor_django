#!/bin/bash
# Script para iniciar o Django Factoring System no Linux/Mac

clear

cat << "EOF"

======================================
  FACTORING SYSTEM - Django Setup
======================================

EOF

# Verificar se Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "[ERRO] Python 3 não está instalado"
    exit 1
fi

# Criar ambiente virtual se não existir
if [ ! -d "venv" ]; then
    echo "[1/5] Criando ambiente virtual..."
    python3 -m venv venv
    echo "[OK] Ambiente virtual criado"
fi

# Ativar ambiente virtual
echo "[2/5] Ativando ambiente virtual..."
source venv/bin/activate
echo "[OK] Ambiente ativado"

# Instalar dependências
echo "[3/5] Instalando dependências..."
pip install -q -r requirements.txt
echo "[OK] Dependências instaladas"

# Executar migrations
echo "[4/5] Configurando banco de dados..."
python manage.py migrate -q
echo "[OK] Banco de dados configurado"

# Criar superusuário se não existir
python manage.py shell -c "
from django.contrib.auth.models import User
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@factoring.com', 'admin123')
    print('[OK] Superusuário admin criado (usuario: admin, senha: admin123)')
else:
    print('[OK] Superusuário já existe')
"

# Carregar dados de exemplo
echo "[5/5] Carregando dados de exemplo..."
python manage.py shell < setup_dados_exemplo.py

cat << "EOF"

======================================
  SETUP CONCLUÍDO COM SUCESSO!
======================================

Iniciando servidor Django...
URL: http://127.0.0.1:8000
Admin: http://127.0.0.1:8000/admin
Credenciais: admin / admin123

Pressione CTRL+C para parar o servidor

EOF

python manage.py runserver
