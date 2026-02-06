# Script para popular o banco de dados com dados de exemplo
# Executar: python manage.py shell < setup_dados_exemplo.py

from factoring_app.models import (
    Banco, Agencia, ContaBancaria, Cliente, Sacado, Agente,
    TipoDocumento, Ocorrencia, Bordero, Documento, Cheque,
    Pagamento, Feriado, ParametrosGerais
)
from datetime import datetime, timedelta
from decimal import Decimal

# Criar Bancos
print("Criando bancos...")
bancos_data = [
    {'codigo': '001', 'nome': 'Banco do Brasil', 'descricao': 'Banco Estatal'},
    {'codigo': '033', 'nome': 'Banco Santander', 'descricao': 'Banco Privado'},
    {'codigo': '104', 'nome': 'Caixa Econômica Federal', 'descricao': 'Banco Estatal'},
]

for banco_data in bancos_data:
    banco, created = Banco.objects.get_or_create(
        codigo=banco_data['codigo'],
        defaults={'nome': banco_data['nome'], 'descricao': banco_data['descricao']}
    )
    if created:
        print(f"✓ Banco {banco.nome} criado")

# Criar Agências
print("\nCriando agências...")
bb = Banco.objects.get(codigo='001')
agencia, created = Agencia.objects.get_or_create(
    banco=bb,
    numero='0001',
    defaults={
        'nome': 'Agência Centro',
        'endereco': 'Rua Principal, 100',
        'telefone': '(11) 3333-3333'
    }
)
if created:
    print(f"✓ Agência {agencia.nome} criada")

# Criar Contas Bancárias
print("\nCriando contas bancárias...")
conta, created = ContaBancaria.objects.get_or_create(
    agencia=agencia,
    numero='123456',
    defaults={
        'tipo_conta': 'corrente',
        'saldo': Decimal('50000.00'),
        'ativa': True,
    }
)
if created:
    print(f"✓ Conta {conta.numero} criada")

# Criar Clientes
print("\nCriando clientes...")
clientes_data = [
    {
        'nome': 'Empresa ABC Ltda',
        'tipo_pessoa': 'pj',
        'cpf_cnpj': '12.345.678/0001-90',
        'email': 'contato@empresaabc.com',
        'limite_credito': Decimal('100000.00'),
    },
    {
        'nome': 'João Silva',
        'tipo_pessoa': 'pf',
        'cpf_cnpj': '123.456.789-10',
        'email': 'joao@email.com',
        'limite_credito': Decimal('50000.00'),
    },
    {
        'nome': 'Empresa XYZ Comércio',
        'tipo_pessoa': 'pj',
        'cpf_cnpj': '98.765.432/0001-10',
        'email': 'vendas@xyzcomercio.com',
        'limite_credito': Decimal('150000.00'),
    },
]

clientes = []
for cliente_data in clientes_data:
    cliente, created = Cliente.objects.get_or_create(
        cpf_cnpj=cliente_data['cpf_cnpj'],
        defaults=cliente_data
    )
    if created:
        clientes.append(cliente)
        print(f"✓ Cliente {cliente.nome} criado")
    else:
        clientes.append(cliente)

# Criar Sacados
print("\nCriando sacados...")
if clientes:
    cliente = clientes[0]
    sacado, created = Sacado.objects.get_or_create(
        cliente=cliente,
        cpf_cnpj='111.111.111-11',
        defaults={
            'nome': 'Pedro Santos',
            'email': 'pedro@email.com',
            'telefone': '(11) 99999-9999',
        }
    )
    if created:
        print(f"✓ Sacado {sacado.nome} criado")

# Criar Agentes
print("\nCriando agentes...")
agente, created = Agente.objects.get_or_create(
    cpf='555.555.555-55',
    defaults={
        'nome': 'Carlos Mendes',
        'email': 'carlos@factoring.com',
        'departamento': 'Cobrança',
    }
)
if created:
    print(f"✓ Agente {agente.nome} criado")

# Criar Tipos de Documentos
print("\nCriando tipos de documentos...")
tipos_documento = [
    {'codigo': '01', 'descricao': 'Nota Promissória'},
    {'codigo': '02', 'descricao': 'Duplicata'},
    {'codigo': '03', 'descricao': 'Cheque'},
]

for tipo_data in tipos_documento:
    tipo, created = TipoDocumento.objects.get_or_create(
        codigo=tipo_data['codigo'],
        defaults={'descricao': tipo_data['descricao']}
    )
    if created:
        print(f"✓ Tipo {tipo.descricao} criado")

# Criar Ocorrências
print("\nCriando ocorrências...")
ocorrencias_data = [
    {'codigo': '01', 'descricao': 'Pagamento Realizado', 'tipo': 'positiva'},
    {'codigo': '02', 'descricao': 'Cheque Devolvido', 'tipo': 'negativa'},
    {'codigo': '03', 'descricao': 'Título Protestado', 'tipo': 'negativa'},
]

for ocor_data in ocorrencias_data:
    ocorrencia, created = Ocorrencia.objects.get_or_create(
        codigo=ocor_data['codigo'],
        defaults={'descricao': ocor_data['descricao'], 'tipo': ocor_data['tipo']}
    )
    if created:
        print(f"✓ Ocorrência {ocorrencia.descricao} criada")

# Criar Borderos
print("\nCriando borderos...")
if clientes:
    bordero, created = Bordero.objects.get_or_create(
        numero='BORD001',
        defaults={
            'cliente': clientes[0],
            'banco': bb,
            'status': 'novo',
            'valor_total': Decimal('10000.00'),
            'quantidade_titulos': 1,
        }
    )
    if created:
        print(f"✓ Bordero {bordero.numero} criado")

# Criar Feriados
print("\nCriando feriados...")
feriados_data = [
    {'data': datetime(2026, 1, 1).date(), 'descricao': 'Ano Novo', 'tipo': 'nacional'},
    {'data': datetime(2026, 12, 25).date(), 'descricao': 'Natal', 'tipo': 'nacional'},
]

for feriado_data in feriados_data:
    feriado, created = Feriado.objects.get_or_create(
        data=feriado_data['data'],
        defaults={'descricao': feriado_data['descricao'], 'tipo': feriado_data['tipo']}
    )
    if created:
        print(f"✓ Feriado {feriado.descricao} criado")

# Criar Parâmetros Gerais
print("\nCriando parâmetros gerais...")
parametros = [
    {'chave': 'EMPRESA_NOME', 'valor': 'Factoring System', 'tipo': 'string'},
    {'chave': 'TAXA_DESCONTO_PADRAO', 'valor': '2.5', 'tipo': 'numero'},
    {'chave': 'DIAS_VENCIMENTO_PADRAO', 'valor': '30', 'tipo': 'numero'},
]

for param in parametros:
    parametro, created = ParametrosGerais.objects.get_or_create(
        chave=param['chave'],
        defaults={
            'valor': param['valor'],
            'tipo': param['tipo'],
        }
    )
    if created:
        print(f"✓ Parâmetro {parametro.chave} criado")

print("\n✓ Dados de exemplo carregados com sucesso!")

