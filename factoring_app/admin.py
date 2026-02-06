from django.contrib import admin
from django.utils.html import format_html
from . import models

@admin.register(models.UsuarioPermissao)
class UsuarioPermissaoAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'tipo_usuario', 'permissao_incluir', 'permissao_atualizar', 'permissao_excluir')
    list_filter = ('tipo_usuario', 'data_criacao')
    search_fields = ('usuario__username',)


@admin.register(models.Banco)
class BancoAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'nome')
    search_fields = ('codigo', 'nome')


@admin.register(models.Agencia)
class AgenciaAdmin(admin.ModelAdmin):
    list_display = ('banco', 'numero', 'nome', 'telefone')
    list_filter = ('banco',)
    search_fields = ('numero', 'nome')


@admin.register(models.ContaBancaria)
class ContaBancariaAdmin(admin.ModelAdmin):
    list_display = ('numero', 'agencia', 'tipo_conta', 'saldo', 'ativa')
    list_filter = ('tipo_conta', 'ativa', 'agencia__banco')
    search_fields = ('numero',)


@admin.register(models.Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'nome', 'tipo_pessoa', 'cpf_cnpj', 'email', 'limit_credito_display', 'ativo')
    list_filter = ('tipo_pessoa', 'ativo', 'data_cadastro')
    search_fields = ('nome', 'cpf_cnpj')
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('nome', 'tipo_pessoa', 'cpf_cnpj', 'ativo')
        }),
        ('Contato', {
            'fields': ('email', 'telefone')
        }),
        ('Endereço', {
            'fields': ('endereco', 'cidade', 'estado', 'cep')
        }),
        ('Limites e Saldos', {
            'fields': ('limite_credito', 'saldo_devedor')
        }),
    )
    
    def limit_credito_display(self, obj):
        return f"R$ {obj.limite_credito:,.2f}"
    limit_credito_display.short_description = 'Limite de Crédito'


@admin.register(models.Sacado)
class SacadoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'cliente', 'cpf_cnpj', 'email')
    list_filter = ('cliente',)
    search_fields = ('nome', 'cpf_cnpj')


@admin.register(models.Agente)
class AgenteAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'nome', 'cpf', 'email', 'departamento', 'ativo')
    list_filter = ('ativo', 'data_cadastro')
    search_fields = ('nome', 'cpf')


@admin.register(models.TipoDocumento)
class TipoDocumentoAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'descricao')
    search_fields = ('codigo', 'descricao')


@admin.register(models.Ocorrencia)
class OcorrenciaAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'descricao', 'tipo', 'ativa')
    list_filter = ('tipo', 'ativa')
    search_fields = ('codigo', 'descricao')


@admin.register(models.Bordero)
class BorderoAdmin(admin.ModelAdmin):
    list_display = ('numero', 'cliente', 'banco', 'status', 'data_criacao', 'valor_total_display')
    list_filter = ('status', 'data_criacao', 'cliente', 'banco')
    search_fields = ('numero', 'cliente__nome')
    readonly_fields = ('data_criacao',)
    
    def valor_total_display(self, obj):
        return f"R$ {obj.valor_total:,.2f}"
    valor_total_display.short_description = 'Valor Total'


@admin.register(models.Documento)
class DocumentoAdmin(admin.ModelAdmin):
    list_display = ('numero_documento', 'sacado', 'bordero', 'valor', 'data_vencimento', 'status')
    list_filter = ('status', 'data_vencimento', 'bordero')
    search_fields = ('numero_documento', 'sacado__nome')
    readonly_fields = ('numero_sequencial',)


@admin.register(models.Cheque)
class ChequeAdmin(admin.ModelAdmin):
    list_display = ('numero', 'conta_bancaria', 'beneficiario', 'valor', 'status')
    list_filter = ('status', 'data_emissao')
    search_fields = ('numero', 'beneficiario')


@admin.register(models.Pagamento)
class PagamentoAdmin(admin.ModelAdmin):
    list_display = ('id_pagamento', 'documento', 'tipo_pagamento', 'valor_pago', 'data_pagamento')
    list_filter = ('tipo_pagamento', 'data_pagamento')
    search_fields = ('documento__numero_documento',)
    readonly_fields = ('id_pagamento', 'data_pagamento')


@admin.register(models.LiquidacaoBordero)
class LiquidacaoBorderoAdmin(admin.ModelAdmin):
    list_display = ('bordero', 'data_liquidacao', 'valor_liquido_display')
    list_filter = ('data_liquidacao',)
    search_fields = ('bordero__numero',)
    
    def valor_liquido_display(self, obj):
        return f"R$ {obj.valor_liquido:,.2f}"
    valor_liquido_display.short_description = 'Valor Líquido'


@admin.register(models.Feriado)
class FeriadoAdmin(admin.ModelAdmin):
    list_display = ('data', 'descricao', 'tipo', 'estado')
    list_filter = ('tipo', 'data')
    search_fields = ('descricao',)


@admin.register(models.ParametrosGerais)
class ParametrosGeraisAdmin(admin.ModelAdmin):
    list_display = ('chave', 'valor', 'tipo')
    list_filter = ('tipo',)
    search_fields = ('chave', 'descricao')


@admin.register(models.LogOperacao)
class LogOperacaoAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'tipo_operacao', 'tabela', 'data_hora')
    list_filter = ('tipo_operacao', 'data_hora', 'tabela')
    search_fields = ('usuario__username', 'tabela')
    readonly_fields = ('data_hora',)
