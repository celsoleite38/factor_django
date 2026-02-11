@echo off
REM Script para iniciar o Django Factoring System no Windows

cls
color 0A

echo.
echo ======================================
echo   FACTORING SYSTEM - Django Setup
echo ======================================
echo.

REM Verificar se Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERRO] Python não está instalado ou não está no PATH
    exit /b 1
)

REM Criar ambiente virtual se não existir
if not exist "venv" (
    echo [1/5] Criando ambiente virtual...
    python -m venv venv
    echo [OK] Ambiente virtual criado
)

REM Ativar ambiente virtual
echo [2/5] Ativando ambiente virtual...
call venv\Scripts\activate.bat
echo [OK] Ambiente ativado

REM Instalar dependências
echo [3/5] Instalando dependências...
pip install --quiet -r requirements.txt
echo [OK] Dependências instaladas

REM Executar migrations
echo [4/5] Configurando banco de dados...
python manage.py migrate --quiet
echo [OK] Banco de dados configurado

REM Criar superusuário se não existir
python manage.py shell -c "
from django.contrib.auth.models import User
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@factoring.com', 'admin123')
    print('[OK] Superusuário admin criado (usuario: admin, senha: admin123)')
else:
    print('[OK] Superusuário já existe')
"

REM Carregar dados de exemplo
echo [5/5] Carregando dados de exemplo...
python manage.py shell < setup_dados_exemplo.py
echo.

echo.
echo ======================================
echo   SETUP CONCLUÍDO COM SUCESSO!
echo ======================================
echo.
echo Iniciando servidor Django...
echo URL: http://127.0.0.1:8000
echo Admin: http://127.0.0.1:8000/admin
echo Credenciais: admin / admin123
echo.
echo Pressione CTRL+C para parar o servidor
echo.

python manage.py runserver
