from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from decimal import Decimal
import uuid

# ============ USUARIOS E PERMISSOES ============
class UsuarioPermissao(models.Model):
    """Model para permissões do usuário"""
    TIPO_USUARIO = [
        ('admin', 'Administrador'),
        ('gerente', 'Gerente'),
        ('operador', 'Operador'),
        ('visualizador', 'Visualizador'),
    ]
    
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='permissao')
    tipo_usuario = models.CharField(max_length=20, choices=TIPO_USUARIO, default='operador')
    permissao_incluir = models.BooleanField(default=False)
    permissao_atualizar = models.BooleanField(default=False)
    permissao_excluir = models.BooleanField(default=False)
    permissao_consulta = models.BooleanField(default=True)
    data_criacao = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Permissão do Usuário'
        verbose_name_plural = 'Permissões do Usuário'
    
    def __str__(self):
        return f"{self.usuario.username} - {self.get_tipo_usuario_display()}"


# ============ DADOS CADASTRAIS ============
class Banco(models.Model):
    """Model para Bancos"""
    codigo = models.CharField(max_length=10, unique=True)
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True)
    data_criacao = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Banco'
        verbose_name_plural = 'Bancos'
    
    def __str__(self):
        return f"{self.codigo} - {self.nome}"


class Agencia(models.Model):
    """Model para Agências Bancárias"""
    banco = models.ForeignKey(Banco, on_delete=models.CASCADE, related_name='agencias')
    numero = models.CharField(max_length=20)
    nome = models.CharField(max_length=100)
    endereco = models.CharField(max_length=200, blank=True)
    telefone = models.CharField(max_length=20, blank=True)
    
    class Meta:
        verbose_name = 'Agência'
        verbose_name_plural = 'Agências'
        unique_together = ('banco', 'numero')
    
    def __str__(self):
        return f"{self.banco.nome} - Agência {self.numero}"


class ContaBancaria(models.Model):
    """Model para Contas Bancárias"""
    agencia = models.ForeignKey(Agencia, on_delete=models.CASCADE, related_name='contas')
    numero = models.CharField(max_length=20)
    tipo_conta = models.CharField(max_length=50, choices=[
        ('corrente', 'Corrente'),
        ('poupanca', 'Poupança'),
        ('investimento', 'Investimento'),
    ])
    saldo = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    ativa = models.BooleanField(default=True)
    data_abertura = models.DateField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Conta Bancária'
        verbose_name_plural = 'Contas Bancárias'
        unique_together = ('agencia', 'numero')
    
    def __str__(self):
        return f"{self.agencia.banco.nome} - {self.numero}"


class Cliente(models.Model):
    """Model para Clientes"""
    TIPO_PESSOA = [
        ('pf', 'Pessoa Física'),
        ('pj', 'Pessoa Jurídica'),
    ]
    
    codigo = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=150)
    tipo_pessoa = models.CharField(max_length=2, choices=TIPO_PESSOA)
    cpf_cnpj = models.CharField(max_length=20, unique=True)
    email = models.EmailField(blank=True)
    telefone = models.CharField(max_length=20, blank=True)
    endereco = models.CharField(max_length=200, blank=True)
    cidade = models.CharField(max_length=100, blank=True)
    estado = models.CharField(max_length=2, blank=True)
    cep = models.CharField(max_length=10, blank=True)
    limite_credito = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    saldo_devedor = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    ativo = models.BooleanField(default=True)
    data_cadastro = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        ordering = ['nome']
    
    def __str__(self):
        return f"{self.codigo} - {self.nome}"


class Sacado(models.Model):
    """Model para Sacados (devedores)"""
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='sacados')
    nome = models.CharField(max_length=150)
    cpf_cnpj = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    telefone = models.CharField(max_length=20, blank=True)
    endereco = models.CharField(max_length=200, blank=True)
    data_cadastro = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Sacado'
        verbose_name_plural = 'Sacados'
    
    def __str__(self):
        return f"{self.nome}"


class Agente(models.Model):
    """Model para Agentes (funcionários)"""
    codigo = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=150)
    cpf = models.CharField(max_length=20, unique=True)
    email = models.EmailField(blank=True)
    telefone = models.CharField(max_length=20, blank=True)
    departamento = models.CharField(max_length=100, blank=True)
    ativo = models.BooleanField(default=True)
    data_cadastro = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Agente'
        verbose_name_plural = 'Agentes'
    
    def __str__(self):
        return self.nome


# ============ DOCUMENTOS E COBRANÇA ============
class TipoDocumento(models.Model):
    """Model para Tipos de Documento"""
    codigo = models.CharField(max_length=10, unique=True)
    descricao = models.CharField(max_length=100)
    
    class Meta:
        verbose_name = 'Tipo de Documento'
        verbose_name_plural = 'Tipos de Documento'
    
    def __str__(self):
        return self.descricao


class Ocorrencia(models.Model):
    """Model para Ocorrências de Cobrança"""
    codigo = models.CharField(max_length=10, unique=True)
    descricao = models.CharField(max_length=200)
    tipo = models.CharField(max_length=20, choices=[
        ('positiva', 'Positiva'),
        ('negativa', 'Negativa'),
        ('informativa', 'Informativa'),
    ])
    ativa = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = 'Ocorrência'
        verbose_name_plural = 'Ocorrências'
    
    def __str__(self):
        return f"{self.codigo} - {self.descricao}"


class Bordero(models.Model):
    """Model para Bordero/Remessa de Cobrança"""
    STATUS_CHOICES = [
        ('novo', 'Novo'),
        ('processando', 'Processando'),
        ('enviado', 'Enviado'),
        ('concluido', 'Concluído'),
        ('cancelado', 'Cancelado'),
    ]
    
    numero = models.CharField(max_length=20, unique=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT)
    banco = models.ForeignKey(Banco, on_delete=models.PROTECT)
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_envio = models.DateField(null=True, blank=True)
    data_retorno = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='novo')
    valor_total = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    quantidade_titulos = models.IntegerField(default=0)
    observacoes = models.TextField(blank=True)
    
    class Meta:
        verbose_name = 'Bordero'
        verbose_name_plural = 'Borderos'
        ordering = ['-data_criacao']
    
    def __str__(self):
        return f"Bordero {self.numero} - {self.cliente.nome}"


class Documento(models.Model):
    """Model para Documentos/Títulos"""
    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('pago', 'Pago'),
        ('cancelado', 'Cancelado'),
        ('devolvido', 'Devolvido'),
    ]
    
    numero_sequencial = models.AutoField(primary_key=True)
    bordero = models.ForeignKey(Bordero, on_delete=models.CASCADE, related_name='documentos')
    tipo_documento = models.ForeignKey(TipoDocumento, on_delete=models.PROTECT)
    sacado = models.ForeignKey(Sacado, on_delete=models.PROTECT)
    numero_documento = models.CharField(max_length=50)
    valor = models.DecimalField(max_digits=15, decimal_places=2)
    data_vencimento = models.DateField()
    data_emissao = models.DateField()
    data_desconto = models.DateField(null=True, blank=True)
    taxa_desconto = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    valor_desconto = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    valor_liquido = models.DecimalField(max_digits=15, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pendente')
    ocorrencia = models.ForeignKey(Ocorrencia, on_delete=models.SET_NULL, null=True, blank=True)
    data_ocorrencia = models.DateField(null=True, blank=True)
    instrucao = models.TextField(blank=True)
    
    class Meta:
        verbose_name = 'Documento'
        verbose_name_plural = 'Documentos'
        ordering = ['data_vencimento']
    
    def __str__(self):
        return f"{self.numero_documento} - {self.sacado.nome}"


class Cheque(models.Model):
    """Model para Cheques"""
    STATUS_CHOICES = [
        ('emitido', 'Emitido'),
        ('compensado', 'Compensado'),
        ('devolvido', 'Devolvido'),
        ('cancelado', 'Cancelado'),
    ]
    
    numero = models.CharField(max_length=20, unique=True)
    conta_bancaria = models.ForeignKey(ContaBancaria, on_delete=models.PROTECT)
    emitente = models.CharField(max_length=150)
    beneficiario = models.CharField(max_length=150)
    valor = models.DecimalField(max_digits=15, decimal_places=2)
    data_emissao = models.DateField()
    data_compensacao = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='emitido')
    motivo_devolucao = models.CharField(max_length=200, blank=True)
    data_devolucao = models.DateField(null=True, blank=True)
    
    class Meta:
        verbose_name = 'Cheque'
        verbose_name_plural = 'Cheques'
    
    def __str__(self):
        return f"Cheque {self.numero}"


# ============ MOVIMENTAÇÕES E PAGAMENTOS ============
class Pagamento(models.Model):
    """Model para Pagamentos"""
    TIPO_PAGAMENTO = [
        ('boleto', 'Boleto'),
        ('cheque', 'Cheque'),
        ('transferencia', 'Transferência'),
        ('dinheiro', 'Dinheiro'),
        ('cartao', 'Cartão'),
    ]
    
    id_pagamento = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    documento = models.ForeignKey(Documento, on_delete=models.CASCADE, related_name='pagamentos')
    tipo_pagamento = models.CharField(max_length=20, choices=TIPO_PAGAMENTO)
    valor_pago = models.DecimalField(max_digits=15, decimal_places=2)
    data_pagamento = models.DateField(auto_now_add=True)
    observacoes = models.TextField(blank=True)
    
    class Meta:
        verbose_name = 'Pagamento'
        verbose_name_plural = 'Pagamentos'
        ordering = ['-data_pagamento']
    
    def __str__(self):
        return f"Pagamento {self.id_pagamento}"


class LiquidacaoBordero(models.Model):
    """Model para Liquidação de Borderos"""
    bordero = models.OneToOneField(Bordero, on_delete=models.CASCADE, related_name='liquidacao')
    data_liquidacao = models.DateField(auto_now_add=True)
    valor_total_recebido = models.DecimalField(max_digits=15, decimal_places=2)
    valor_descontos = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    valor_liquido = models.DecimalField(max_digits=15, decimal_places=2)
    juros_cobrados = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    observacoes = models.TextField(blank=True)
    
    class Meta:
        verbose_name = 'Liquidação de Bordero'
        verbose_name_plural = 'Liquidações de Borderos'
    
    def __str__(self):
        return f"Liquidação {self.bordero.numero}"


# ============ CONFIGURAÇÕES E UTILITÁRIOS ============
class Feriado(models.Model):
    """Model para Feriados"""
    data = models.DateField(unique=True)
    descricao = models.CharField(max_length=100)
    tipo = models.CharField(max_length=20, choices=[
        ('nacional', 'Nacional'),
        ('estadual', 'Estadual'),
        ('municipal', 'Municipal'),
    ])
    estado = models.CharField(max_length=2, blank=True)
    
    class Meta:
        verbose_name = 'Feriado'
        verbose_name_plural = 'Feriados'
        ordering = ['data']
    
    def __str__(self):
        return f"{self.data} - {self.descricao}"


class ParametrosGerais(models.Model):
    """Model para Parâmetros Gerais do Sistema"""
    chave = models.CharField(max_length=100, unique=True)
    valor = models.TextField()
    tipo = models.CharField(max_length=20, choices=[
        ('string', 'Texto'),
        ('numero', 'Número'),
        ('data', 'Data'),
        ('moeda', 'Moeda'),
    ])
    descricao = models.CharField(max_length=200, blank=True)
    
    class Meta:
        verbose_name = 'Parâmetro Geral'
        verbose_name_plural = 'Parâmetros Gerais'
    
    def __str__(self):
        return self.chave


class LogOperacao(models.Model):
    """Model para Log de Operações do Sistema"""
    TIPO_OPERACAO = [
        ('criar', 'Criar'),
        ('atualizar', 'Atualizar'),
        ('deletar', 'Deletar'),
        ('consultar', 'Consultar'),
        ('login', 'Login'),
        ('logout', 'Logout'),
    ]
    
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    data_hora = models.DateTimeField(auto_now_add=True)
    tipo_operacao = models.CharField(max_length=20, choices=TIPO_OPERACAO)
    tabela = models.CharField(max_length=100)
    id_registro = models.IntegerField(null=True, blank=True)
    descricao = models.TextField()
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    
    class Meta:
        verbose_name = 'Log de Operação'
        verbose_name_plural = 'Logs de Operação'
        ordering = ['-data_hora']
    
    def __str__(self):
        return f"{self.usuario} - {self.tipo_operacao} - {self.data_hora}"
