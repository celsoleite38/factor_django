# 📁 Importação de Bancos via XML

## Como Usar

### 1. **Acessar o Admin do Django**
   - Vá para: `http://localhost:8000/admin`
   - Faça login com suas credenciais
   - Procure por "Bancos" no menu de navegação

### 2. **Clicar em "Importar XML"**
   - Na página de listagem de Bancos, procure pelo botão/link "Importar XML"
   - Se não aparecer, você pode acessar diretamente via:
     ```
     http://localhost:8000/admin/factoring_app/banco/importar-xml/
     ```

### 3. **Selecionar e Enviar o Arquivo XML**
   - Clique em "Selecione arquivo XML"
   - Escolha um arquivo `.xml` com a estrutura correta
   - Clique em "Importar Bancos"

### 4. **Ver Resultado**
   - A página exibirá um resumo com:
     - Quantidade de bancos criados/atualizados
     - Quantidade de agências criadas/atualizadas
     - Quantidade de contas criadas/atualizadas
     - Lista de qualquer erro encontrado

---

## Formato do Arquivo XML

O arquivo XML deve seguir esta estrutura:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<bancos>
    <banco>
        <codigo>001</codigo>
        <nome>Banco do Brasil S.A.</nome>
        <descricao>Descrição do banco</descricao>
        <agencias>
            <agencia>
                <numero>0001</numero>
                <nome>Nome da Agência</nome>
                <endereco>Rua/Av., Número - Cidade - Estado</endereco>
                <telefone>(XX) XXXX-XXXX</telefone>
                <contas>
                    <conta>
                        <numero>123456-7</numero>
                        <tipo_conta>corrente</tipo_conta>
                        <saldo>10000.00</saldo>
                        <ativa>true</ativa>
                    </conta>
                </contas>
            </agencia>
        </agencias>
    </banco>
</bancos>
```

---

## Descrição dos Campos

### Banco
| Campo       | Tipo   | Obrigatório | Descrição |
|------------|--------|------------|-----------|
| codigo     | text   | ✓ Sim     | Código do banco (ex: 001, 033, 104) |
| nome       | text   | ✓ Sim     | Nome completo do banco |
| descricao  | text   | ✗ Não     | Descrição ou tipo do banco |

### Agência
| Campo      | Tipo   | Obrigatório | Descrição |
|-----------|--------|------------|-----------|
| numero    | text   | ✓ Sim     | Número da agência |
| nome      | text   | ✓ Sim     | Nome da agência |
| endereco  | text   | ✗ Não     | Endereço da agência |
| telefone  | text   | ✗ Não     | Telefone da agência |

### Conta
| Campo     | Tipo    | Obrigatório | Descrição |
|-----------|---------|------------|-----------|
| numero    | text    | ✓ Sim     | Número da conta |
| tipo_conta| text    | ✗ Não     | corrente, poupança, investimento |
| saldo     | decimal | ✗ Não     | Saldo inicial (formato: 1000.00) |
| ativa     | boolean | ✗ Não     | true ou false |

---

## Exemplo

Veja o arquivo `exemplo_bancos.xml` na raiz do projeto para um exemplo completo.

---

## Funcionalidades

### ✅ Criar Novos Registros
Se código/número não existir, o sistema cria automaticamente

### ✅ Atualizar Existentes
Se código/número já existe, o sistema atualiza os dados

### ✅ Validação
O sistema valida:
- Campos obrigatórios
- Formato de dados
- Valores válidos

### ✅ Relatório Detalhado
Após importação, exibe:
- Quantidade de registros criados
- Quantidade de registros atualizados
- Lista de erros (se houver)

---

## Dicas

1. **Validar XML**: Antes de importar, valide seu XML usando um validador online
2. **Backup**: Faça backup do banco antes de importações grandes
3. **Teste**: Comece com poucos registros para testar
4. **Códigos de Banco**: Use códigos oficiais do BACEN
   - 001 = Banco do Brasil
   - 033 = Banco Santander
   - 104 = Caixa Econômica Federal
   - Ver lista completa: https://www.bcb.gov.br/pom/spb/participantes.html

---

## Troubleshooting

### Erro: "Arquivo inválido ou não é XML"
- Verifique se o arquivo é um XML válido
- Use uma ferramenta de validação XML

### Erro: "Banco sem código ou nome"
- Certifique-se que cada banco tem `codigo` e `nome`

### Erro: "Agência do banco XXX sem número ou nome"
- Verifique se cada agência tem `numero` e `nome`

### Desconto não foi importado
- Este campo não faz parte do escopo de bancos, é para documentos

---

## Script de Importação via Terminal

Você também pode importar via shell do Django:

```python
from factoring_app.bancos_importer import importar_bancos_xml

with open('exemplo_bancos.xml', 'r', encoding='utf-8') as f:
    resultado = importar_bancos_xml(f)
    print(resultado)
```

Execute com:
```bash
python manage.py shell
```
