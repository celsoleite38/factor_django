from django.urls import path
from . import views

urlpatterns = [
    # Autenticação
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # Clientes
    path('clientes/', views.lista_clientes, name='lista_clientes'),
    path('clientes/<int:pk>/', views.detalhe_cliente, name='detalhe_cliente'),
    path('clientes/criar/', views.criar_cliente, name='criar_cliente'),
    
    # Borderos
    path('borderos/', views.lista_borderos, name='lista_borderos'),
    path('borderos/<int:pk>/', views.detalhe_bordero, name='detalhe_bordero'),
    
    # Documentos
    path('documentos/', views.lista_documentos, name='lista_documentos'),
    path('documentos/<int:pk>/', views.detalhe_documento, name='detalhe_documento'),
    
    # Bancos
    path('bancos/', views.lista_bancos, name='lista_bancos'),
    path('bancos/<int:pk>/', views.detalhe_banco, name='detalhe_banco'),
    
    # Relatórios
    path('relatorios/pendencias/', views.relatorio_pendencias, name='relatorio_pendencias'),
    path('relatorios/fluxo-caixa/', views.relatorio_fluxo_caixa, name='relatorio_fluxo_caixa'),
    path('relatorios/clientes/', views.relatorio_clientes, name='relatorio_clientes'),
]
