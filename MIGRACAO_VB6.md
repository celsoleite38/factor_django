# Se você já tem um banco de dados do VB6 e quer migrar os dados:

## PASSO 1: Exportar dados do VB6

### Opção A: Exportar para CSV ou Excel
1. No VB6, use a funcionalidade de exportar dados de cada tabela
2. Salve em formato CSV ou Excel
3. Coloque os arquivos em uma pasta "dados_vb6"

### Opção B: Exportar para SQL
1. Se o VB6 usa SQL Server, use SQL Server Management Studio
2. Se usa Access, use ferramentas de exportação do Access

---

## PASSO 2: Importar dados para Django

Crie um script de importação personalizado:

```python
# import_dados_vb6.py
import csv
from factoring_app.models import Cliente, Banco, Bordero, Documento
from decimal import Decimal

# Exemplo: Importar clientes
with open('dados_vb6/clientes.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        Cliente.objects.create(
            codigo=int(row['codigo']),
            nome=row['nome'],
            tipo_pessoa=row['tipo_pessoa'],
            cpf_cnpj=row['cpf_cnpj'],
            email=row.get('email', ''),
            limite_credito=Decimal(row['limite_credito']),
        )
        print(f"Cliente {row['codigo']} importado")

print("Importação concluída!")
```

Execute:
```bash
python manage.py shell < import_dados_vb6.py
```

---

## Tipagem de Campos - Mapeamento VB6 para Django

| VB6 | Django | Exemplo |
|-----|--------|---------|
| String | CharField | `CharField(max_length=100)` |
| Currency | DecimalField | `DecimalField(max_digits=15, decimal_places=2)` |
| Date | DateField | `DateField()` |
| DateTime | DateTimeField | `DateTimeField()` |
| Integer | IntegerField | `IntegerField()` |
| Boolean | BooleanField | `BooleanField(default=False)` |

---

## Validação de Dados

Após importar, validar a integridade:

```python
# validate_import.py
from factoring_app.models import Cliente, Bordero, Documento

print(f"Total de clientes: {Cliente.objects.count()}")
print(f"Total de borderos: {Bordero.objects.count()}")
print(f"Total de documentos: {Documento.objects.count()}")

# Verificar clientes sem nome (inválido)
clientes_invalidos = Cliente.objects.filter(nome='')
print(f"Clientes sem nome: {clientes_invalidos.count()}")

# Verificar documentos com data inválida
from django.db.models import Q
from datetime import datetime
documentos_invalidos = Documento.objects.filter(
    Q(data_vencimento__lt=datetime(2000, 1, 1)) |
    Q(data_vencimento__gt=datetime(2100, 1, 1))
)
print(f"Documentos com data inválida: {documentos_invalidos.count()}")
```

---

## Notas Importantes

1. **Backup**: Sempre faça backup dos dados do VB6 antes de qualquer migração
2. **Integridade Referencial**: Certifique-se de que as relações entre tabelas estão corretas
3. **CPF/CNPJ**: Valide os valores antes de importar
4. **Datas**: Certifique-se de que o formato de data está correto
5. **Valores Decimais**: Use Decimal() para evitar problemas com ponto flutuante
6. **Encoding**: Se houver caracteres especiais, certifique-se de usar UTF-8

---

## Teste a Migração em Ambiente de Teste Primeiro!

```bash
# Fazer backup do banco de dados
cp db.sqlite3 db.sqlite3.backup

# Criar novo banco de teste
rm db.sqlite3
python manage.py migrate
python manage.py shell < import_dados_vb6.py

# Validar
python manage.py shell < validate_import.py

# Se tudo OK, restore e repita em produção
cp db.sqlite3.backup db.sqlite3
```
