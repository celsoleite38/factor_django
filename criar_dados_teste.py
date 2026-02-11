from factoring_app.models import (
    TipoDocumento, Banco, Agencia, ContaBancaria, 
    Cliente, Sacado, Bordero, Documento
)
from datetime import datetime, timedelta
from decimal import Decimal

print("\n" + "="*60)
print("CRIANDO DADOS DE EXEMPLO PARA TESTAR FACTORING")
print("="*60 + "\n")

# 1. Criar Tipos de Documento
print("1️⃣  Criando Tipos de Documento...")
tipos = [
    ('CHQ', 'Cheque'),
    ('DUP', 'Duplicata'),
    ('NP', 'Nota Promissória'),
    ('PM', 'Promissória'),
    ('CPR', 'Cédula de Produto Rural'),
    ('BOL', 'Boleto Bancário'),
]

for codigo, descricao in tipos:
    tipo, created = TipoDocumento.objects.get_or_create(
        codigo=codigo,
        defaults={'descricao': descricao}
    )
    if created:
        print(f"   ✓ {codigo} - {descricao}")

# 2. Verificar/Criar Bancos
print("\n2️⃣  Preparando Bancos...")
bancos_data = [
    ('001', 'Banco do Brasil'),
    ('033', 'Banco Santander'),
]

bancos = {}
for codigo, nome in bancos_data:
    banco, created = Banco.objects.get_or_create(
        codigo=codigo,
        defaults={'nome': nome}
    )
    bancos[codigo] = banco
    if created:
        print(f"   ✓ {codigo} - {nome}")
    else:
        print(f"   ℹ️  {codigo} - {nome} (já existe)")

# 3. Verificar/Criar Clientes
print("\n3️⃣  Preparando Clientes...")
clientes_data = [
    {
        'nome': 'Distribuidora ABC Ltda',
        'tipo_pessoa': 'pj',
        'cpf_cnpj': '12.345.678/0001-99',
        'email': 'contato@abc.com',
        'limite_credito': Decimal('100000.00')
    },
]

clientes = []
for cliente_data in clientes_data:
    cliente, created = Cliente.objects.get_or_create(
        cpf_cnpj=cliente_data['cpf_cnpj'],
        defaults=cliente_data
    )
    clientes.append(cliente)
    if created:
        print(f"   ✓ {cliente.nome}")
    else:
        print(f"   ℹ️  {cliente.nome} (já existe)")

# 4. Criar Sacados
print("\n4️⃣  Criando Sacados...")
sacados_data = [
    ('João Silva Serviços', '123.456.789-01'),
    ('Maria Oliveira Consultoria', '987.654.321-09'),
    ('Carlos Santos Comércio', '456.789.123-45'),
]

sacados = {}
for nome, cpf_cnpj in sacados_data:
    sacado, created = Sacado.objects.get_or_create(
        cliente=clientes[0],
        cpf_cnpj=cpf_cnpj,
        defaults={'nome': nome}
    )
    sacados[cpf_cnpj] = sacado
    if created:
        print(f"   ✓ {nome}")

# 5. Criar Borderô com Documentos
print("\n5️⃣  Criando Borderô de Teste...")

tipo_cheque = TipoDocumento.objects.get(codigo='CHQ')
tipo_duplicata = TipoDocumento.objects.get(codigo='DUP')
tipo_np = TipoDocumento.objects.get(codigo='NP')

banco = bancos['001']
cliente = clientes[0]

bordero, created = Bordero.objects.get_or_create(
    numero='BRD-001-2025',
    defaults={
        'cliente': cliente,
        'banco': banco,
        'data_envio': datetime.now().date(),
        'status': 'novo',
        'valor_total': Decimal('0'),
        'quantidade_titulos': 0,
        'observacoes': 'Borderô de teste - Sistema de Factoring'
    }
)

if created:
    print(f"\n   ✓ Borderô {bordero.numero} criado!")
    
    # Criar documentos
    documentos_data = [
        {
            'tipo_documento': tipo_cheque,
            'numero_documento': 'CHQ-001205',
            'sacado': sacados['123.456.789-01'],
            'valor': Decimal('5000.00'),
            'data_vencimento': (datetime.now() + timedelta(days=30)).date(),
            'data_emissao': datetime.now().date(),
        },
        {
            'tipo_documento': tipo_duplicata,
            'numero_documento': 'DUP-002025',
            'sacado': sacados['987.654.321-09'],
            'valor': Decimal('7500.00'),
            'data_vencimento': (datetime.now() + timedelta(days=45)).date(),
            'data_emissao': datetime.now().date(),
        },
        {
            'tipo_documento': tipo_np,
            'numero_documento': 'NP-003025',
            'sacado': sacados['456.789.123-45'],
            'valor': Decimal('3200.50'),
            'data_vencimento': (datetime.now() + timedelta(days=60)).date(),
            'data_emissao': datetime.now().date(),
        },
    ]
    
    valor_total = Decimal('0')
    for doc_data in documentos_data:
        documento, created = Documento.objects.get_or_create(
            bordero=bordero,
            numero_documento=doc_data['numero_documento'],
            defaults={
                'tipo_documento': doc_data['tipo_documento'],
                'sacado': doc_data['sacado'],
                'valor': doc_data['valor'],
                'data_vencimento': doc_data['data_vencimento'],
                'data_emissao': doc_data['data_emissao'],
                'valor_liquido': doc_data['valor'],
                'status': 'pendente'
            }
        )
        if created:
            print(f"   ✓ {doc_data['tipo_documento'].descricao}: {doc_data['numero_documento']} - R$ {doc_data['valor']:,.2f}")
            valor_total += doc_data['valor']
        else:
            valor_total += doc_data['valor']
    
    # Atualizar totalizadores
    bordero.valor_total = valor_total
    bordero.quantidade_titulos = len(documentos_data)
    bordero.save()
    print(f"\n   📊 TOTAL DO BORDERÔ: R$ {valor_total:,.2f} | {len(documentos_data)} documentos")
else:
    print(f"\n   ℹ️  Borderô {bordero.numero} já existe!")

print("\n" + "="*60)
print("✅ DADOS DE TESTE CRIADOS COM SUCESSO!")
print("="*60)
print("\n📋 Próximos passos:")
print("   1. Inicie o servidor: python manage.py runserver")
print("   2. Acesse: http://localhost:8000/login")
print("   3. Vá para Borderos → Lista Borderos para ver o borderô criado")
print("   4. Clique em 'Criar Bordero' para adicionar um novo\n")
