from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q, Sum
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from datetime import datetime, timedelta
from decimal import Decimal
import json

from . import models


# ============ AUTENTICAÇÃO ============
def login_view(request):
    """View para login do usuário"""
    # Se já está autenticado, vai direto para o dashboard
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            # Registra log (desabilitado temporariamente)
            # try:
            #     models.LogOperacao.objects.create(
            #         usuario=user,
            #         tipo_operacao='login',
            #         tabela='Auth',
            #         descricao=f'Login de {user.username}',
            #         ip_address=request.META.get('REMOTE_ADDR')
            #     )
            # except:
            #     pass
            messages.success(request, f'Bem-vindo, {user.first_name or user.username}!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Usuário ou senha incorretos!')
    
    return render(request, 'factoring_app/login.html')


def logout_view(request):
    """View para logout do usuário"""
    # Registra log (desabilitado temporariamente)
    # try:
    #     models.LogOperacao.objects.create(
    #         usuario=request.user,
    #         tipo_operacao='logout',
    #         tabela='Auth',
    #         descricao=f'Logout de {request.user.username}',
    #         ip_address=request.META.get('REMOTE_ADDR')
    #     )
    # except:
    #     pass
    logout(request)
    messages.success(request, 'Logout realizado com sucesso!')
    return redirect('login')


# ============ DASHBOARD ============
@login_required(login_url='login')
def dashboard(request):
    """View do dashboard principal"""
    context = {
        'total_clientes': models.Cliente.objects.filter(ativo=True).count(),
        'total_borderos': models.Bordero.objects.count(),
        'total_documentos': models.Documento.objects.count(),
        'valor_total_pendente': models.Documento.objects.filter(status='pendente').aggregate(Sum('valor'))['valor__sum'] or 0,
        'borderos_recentes': models.Bordero.objects.all()[:5],
        'documentos_vencidos': models.Documento.objects.filter(
            status='pendente',
            data_vencimento__lt=datetime.now().date()
        ).count(),
    }
    return render(request, 'factoring_app/dashboard.html', context)


# ============ CLIENTES ============
@login_required(login_url='login')
def lista_clientes(request):
    """Lista todos os clientes"""
    clientes = models.Cliente.objects.all()
    
    # Filtros
    if request.GET.get('nome'):
        clientes = clientes.filter(nome__icontains=request.GET.get('nome'))
    if request.GET.get('cpf_cnpj'):
        clientes = clientes.filter(cpf_cnpj=request.GET.get('cpf_cnpj'))
    if request.GET.get('ativo') == 'true':
        clientes = clientes.filter(ativo=True)
    elif request.GET.get('ativo') == 'false':
        clientes = clientes.filter(ativo=False)
    
    context = {
        'clientes': clientes.order_by('nome'),
        'total': clientes.count(),
    }
    return render(request, 'factoring_app/clientes/lista.html', context)


@login_required(login_url='login')
def detalhe_cliente(request, pk):
    """Detalhes de um cliente"""
    cliente = get_object_or_404(models.Cliente, pk=pk)
    borderos = models.Bordero.objects.filter(cliente=cliente)
    sacados = models.Sacado.objects.filter(cliente=cliente)
    
    context = {
        'cliente': cliente,
        'borderos': borderos,
        'sacados': sacados,
        'total_documentos': models.Documento.objects.filter(
            bordero__cliente=cliente
        ).count(),
    }
    return render(request, 'factoring_app/clientes/detalhe.html', context)


@login_required(login_url='login')
def criar_cliente(request):
    """Cria novo cliente"""
    if request.method == 'POST':
        try:
            cliente = models.Cliente.objects.create(
                nome=request.POST.get('nome'),
                tipo_pessoa=request.POST.get('tipo_pessoa'),
                cpf_cnpj=request.POST.get('cpf_cnpj'),
                email=request.POST.get('email', ''),
                telefone=request.POST.get('telefone', ''),
                endereco=request.POST.get('endereco', ''),
                cidade=request.POST.get('cidade', ''),
                estado=request.POST.get('estado', ''),
                cep=request.POST.get('cep', ''),
                limite_credito=Decimal(request.POST.get('limite_credito', 0)),
            )
            
            # Registra log
            models.LogOperacao.objects.create(
                usuario=request.user,
                tipo_operacao='criar',
                tabela='Cliente',
                id_registro=cliente.codigo,
                descricao=f'Criação de cliente: {cliente.nome}',
            )
            
            messages.success(request, 'Cliente criado com sucesso!')
            return redirect('detalhe_cliente', pk=cliente.codigo)
        except Exception as e:
            messages.error(request, f'Erro ao criar cliente: {str(e)}')
    
    return render(request, 'factoring_app/clientes/criar.html')


# ============ BORDEROS ============
@login_required(login_url='login')
def lista_borderos(request):
    """Lista borderos"""
    borderos = models.Bordero.objects.all()
    
    # Filtros
    if request.GET.get('cliente'):
        borderos = borderos.filter(cliente__nome__icontains=request.GET.get('cliente'))
    if request.GET.get('status'):
        borderos = borderos.filter(status=request.GET.get('status'))
    
    context = {
        'borderos': borderos.order_by('-data_criacao'),
        'total': borderos.count(),
        'status_choices': models.Bordero.STATUS_CHOICES,
    }
    return render(request, 'factoring_app/borderos/lista.html', context)


@login_required(login_url='login')
def detalhe_bordero(request, pk):
    """Detalhes do bordero"""
    bordero = get_object_or_404(models.Bordero, pk=pk)
    documentos = models.Documento.objects.filter(bordero=bordero)
    
    context = {
        'bordero': bordero,
        'documentos': documentos,
        'total_valor': documentos.aggregate(Sum('valor'))['valor__sum'] or 0,
        'total_documentos': documentos.count(),
    }
    return render(request, 'factoring_app/borderos/detalhe.html', context)


# ============ DOCUMENTOS ============
@login_required(login_url='login')
def lista_documentos(request):
    """Lista documentos"""
    documentos = models.Documento.objects.all()
    
    # Filtros
    if request.GET.get('status'):
        documentos = documentos.filter(status=request.GET.get('status'))
    if request.GET.get('vencimento_inicio'):
        documentos = documentos.filter(
            data_vencimento__gte=request.GET.get('vencimento_inicio')
        )
    if request.GET.get('vencimento_fim'):
        documentos = documentos.filter(
            data_vencimento__lte=request.GET.get('vencimento_fim')
        )
    
    context = {
        'documentos': documentos.order_by('data_vencimento'),
        'total': documentos.count(),
        'vencidos': documentos.filter(
            status='pendente',
            data_vencimento__lt=datetime.now().date()
        ).count(),
        'proximos_vencer': documentos.filter(
            status='pendente',
            data_vencimento__gte=datetime.now().date(),
            data_vencimento__lte=datetime.now().date() + timedelta(days=7)
        ).count(),
        'status_choices': models.Documento.STATUS_CHOICES,
    }
    return render(request, 'factoring_app/documentos/lista.html', context)


@login_required(login_url='login')
def detalhe_documento(request, pk):
    """Detalhes do documento"""
    documento = get_object_or_404(models.Documento, pk=pk)
    pagamentos = models.Pagamento.objects.filter(documento=documento)
    
    context = {
        'documento': documento,
        'pagamentos': pagamentos,
        'total_pago': pagamentos.aggregate(Sum('valor_pago'))['valor_pago__sum'] or 0,
    }
    return render(request, 'factoring_app/documentos/detalhe.html', context)


# ============ BANCOS ============
@login_required(login_url='login')
def lista_bancos(request):
    """Lista bancos"""
    bancos = models.Banco.objects.all()
    context = {'bancos': bancos}
    return render(request, 'factoring_app/bancos/lista.html', context)


@login_required(login_url='login')
def detalhe_banco(request, pk):
    """Detalhes do banco"""
    banco = get_object_or_404(models.Banco, pk=pk)
    agencias = models.Agencia.objects.filter(banco=banco)
    
    context = {
        'banco': banco,
        'agencias': agencias,
    }
    return render(request, 'factoring_app/bancos/detalhe.html', context)


# ============ RELATÓRIOS ============
@login_required(login_url='login')
def relatorio_pendencias(request):
    """Relatório de pendências"""
    documentos = models.Documento.objects.filter(status='pendente').order_by('data_vencimento')
    
    total_valor = documentos.aggregate(Sum('valor'))['valor__sum'] or 0
    vencidos = documentos.filter(data_vencimento__lt=datetime.now().date())
    
    context = {
        'documentos': documentos,
        'total_valor': total_valor,
        'total_documentos': documentos.count(),
        'documentos_vencidos': vencidos.count(),
        'valor_vencido': vencidos.aggregate(Sum('valor'))['valor__sum'] or 0,
    }
    return render(request, 'factoring_app/relatorios/pendencias.html', context)


@login_required(login_url='login')
def relatorio_fluxo_caixa(request):
    """Relatório de fluxo de caixa"""
    data_inicio = request.GET.get('data_inicio') or (datetime.now() - timedelta(days=30)).date()
    data_fim = request.GET.get('data_fim') or datetime.now().date()
    
    pagamentos = models.Pagamento.objects.filter(
        data_pagamento__range=[data_inicio, data_fim]
    ).order_by('data_pagamento')
    
    total_recebido = pagamentos.aggregate(Sum('valor_pago'))['valor_pago__sum'] or 0
    
    # Agrupado por tipo de pagamento
    por_tipo = {}
    for pagamento in pagamentos:
        tipo = pagamento.get_tipo_pagamento_display()
        if tipo not in por_tipo:
            por_tipo[tipo] = 0
        por_tipo[tipo] += pagamento.valor_pago
    
    context = {
        'pagamentos': pagamentos,
        'total_recebido': total_recebido,
        'por_tipo': por_tipo,
        'data_inicio': data_inicio,
        'data_fim': data_fim,
    }
    return render(request, 'factoring_app/relatorios/fluxo_caixa.html', context)


@login_required(login_url='login')
def relatorio_clientes(request):
    """Relatório de clientes"""
    clientes = models.Cliente.objects.annotate(
        total_documentos=models.Count('sacado__numero_sequencial', distinct=True),
        saldo_total=models.Sum('saldo_devedor')
    )
    
    context = {
        'clientes': clientes.order_by('saldo_total'),
        'total_clientes': clientes.count(),
    }
    return render(request, 'factoring_app/relatorios/clientes.html', context)
