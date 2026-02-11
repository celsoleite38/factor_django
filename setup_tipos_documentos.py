"""
Script para criar os tipos de documento padrão do sistema de factoring.
Executar com: python manage.py shell < setup_tipos_documentos.py
"""

from factoring_app.models import TipoDocumento

# Lista de tipos de documento comuns em factoring
tipos = [
    {
        'codigo': 'CHQ',
        'descricao': 'Cheque'
    },
    {
        'codigo': 'DUP',
        'descricao': 'Duplicata'
    },
    {
        'codigo': 'NP',
        'descricao': 'Nota Promissória'
    },
    {
        'codigo': 'PM',
        'descricao': 'Promissória'
    },
    {
        'codigo': 'CPR',
        'descricao': 'Cédula de Produto Rural'
    },
    {
        'codigo': 'BOL',
        'descricao': 'Boleto Bancário'
    },
    {
        'codigo': 'REC',
        'descricao': 'Recibo'
    },
    {
        'codigo': 'OUT',
        'descricao': 'Outro'
    },
]

print("Criando tipos de documento...")
for tipo_data in tipos:
    tipo, created = TipoDocumento.objects.get_or_create(
        codigo=tipo_data['codigo'],
        defaults={'descricao': tipo_data['descricao']}
    )
    if created:
        print(f"✓ Criado: {tipo.codigo} - {tipo.descricao}")
    else:
        print(f"✓ Já existe: {tipo.codigo} - {tipo.descricao}")

print("\nTipos de documento configurados com sucesso!")
