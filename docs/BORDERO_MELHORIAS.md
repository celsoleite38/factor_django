# Melhorias no Borderô - Adição de Documentos

## O que foi alterado:

### 1. **Modelo de Documento** (models.py)
- Já existia, mas agora é totalmente integrado ao formulário de criação de borderô
- Campos principais:
  - `tipo_documento`: Tipo de documento (Cheque, Promissória, Duplicata, etc.)
  - `numero_documento`: Número identificador
  - `valor`: Valor do documento
  - `data_vencimento`: Data quando o documento vence
  - `data_emissao`: Data de emissão
  - `valor_liquido`: Valor após descontos

### 2. **Formulário de Documento** (forms.py)
- Novo `DocumentoForm` para validação de documentos
- Campos para dados do devedor (sacado):
  - Nome do devedor
  - CPF/CNPJ do devedor

### 3. **Template de Criação** (templates/factoring_app/borderos/criar.html)
- Interface melhorada com duas seções:
  - **Dados do Borderô**: Número, Cliente, Banco, Data, Observações
  - **Documentos**: Adicionar múltiplos documentos dinamicamente
  
- **Botão "+ Adicionar Documento"**: Permite adicionar quantos documentos forem necessários
- **Card dinâmico para cada documento** com campos:
  - Tipo de Documento (Cheque, Promissória, Duplicata, Nota Promissória, CPR, etc.)
  - Número do Documento
  - Nome do Devedor
  - CPF/CNPJ do Devedor
  - Valor
  - Data de Vencimento
  - Data de Emissão
  - Valor Líquido

### 4. **View de Criação** (views.py - função `criar_bordero`)
- Agora processa os documentos junto com o borderô
- Cria/atualiza os sacados (devedores) automaticamente
- Calcula totalizadores do borderô:
  - `valor_total`: Soma de todos os documentos
  - `quantidade_titulos`: Quantidade de documentos adicionados

### 5. **Script de Setup** (setup_tipos_documentos.py)
- Cria os tipos de documento padrão do sistema:
  - CHQ - Cheque
  - DUP - Duplicata
  - NP - Nota Promissória
  - PM - Promissória
  - CPR - Cédula de Produto Rural
  - BOL - Boleto Bancário
  - REC - Recibo
  - OUT - Outro

## Como usar:

### 1. **Primeira vez - Popular tipos de documento:**
```bash
python manage.py shell < setup_tipos_documentos.py
```

### 2. **Criar um novo Borderô:**
1. Ir para "Borderos" → "Criar Borderô"
2. Preencher dados do borderô (Número, Cliente, Banco)
3. Clicar em "+ Adicionar Documento"
4. Preencher dados do documento:
   - Selecionar o tipo (Cheque, Promissória, etc.)
   - Informar número, valor, datas, etc.
   - Informar dados do devedor
5. Para adicionar mais documentos, clicar "+ Adicionar Documento" novamente
6. Para remover um documento, clicar no botão "× Remover" no card
7. Clicar em "Criar Borderô" para finalizar

## Validações:

- ✅ Todos os campos são obrigatórios
- ✅ Mínimo de 1 documento é requerido
- ✅ Valores devem ser decimais positivos
- ✅ Datas devem estar em formato válido
- ✅ Sacados são criados automaticamente se não existirem

## Melhorias de Interface:

- 🎨 Interface com cores diferenciadas (azul para borderô, verde para documentos)
- 📱 Responsivo - funciona em dispositivos móveis
- ⚡ JavaScript dinâmico - adicione/remova documentos sem recarregar
- 🔔 Mensagens de feedback ao usuário
- 📊 Totalizadores automáticos

## Próximas melhorias sugeridas:

1. Adicionar campo de desconto por documento
2. Permitir editar documentos após criação do borderô
3. Importar documentos de arquivo (CSV/Excel)
4. Gerar boletos automaticamente
5. Integração com bancos para retorno de cobrança
