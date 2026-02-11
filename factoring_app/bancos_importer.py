"""
Módulo para importação e exportação de dados de Bancos em XML
"""

import xml.etree.ElementTree as ET
from decimal import Decimal
from .models import Banco, Agencia, ContaBancaria


def exportar_bancos_xml(bancos_queryset=None):
    """
    Exporta bancos, agências e contas para XML.
    
    Args:
        bancos_queryset: QuerySet de bancos (se None, exporta todos)
    
    Returns:
        String com o XML formatado
    """
    if bancos_queryset is None:
        bancos_queryset = Banco.objects.all()
    
    # Cria elemento raiz
    root = ET.Element('bancos')
    root.set('xmlns', 'http://www.example.com/bancos')
    root.set('xmlns:xsi', 'http://www.w3.org/2001/XMLSchema-instance')
    root.set('generated', 'true')
    
    for banco in bancos_queryset:
        banco_elem = ET.SubElement(root, 'banco')
        
        # Adiciona dados do banco
        ET.SubElement(banco_elem, 'codigo').text = str(banco.codigo)
        ET.SubElement(banco_elem, 'nome').text = str(banco.nome)
        if banco.descricao:
            ET.SubElement(banco_elem, 'descricao').text = str(banco.descricao)
        
        # Adiciona agências
        agencias = banco.agencias.all()
        if agencias.exists():
            agencias_elem = ET.SubElement(banco_elem, 'agencias')
            
            for agencia in agencias:
                agencia_elem = ET.SubElement(agencias_elem, 'agencia')
                
                ET.SubElement(agencia_elem, 'numero').text = str(agencia.numero)
                ET.SubElement(agencia_elem, 'nome').text = str(agencia.nome)
                if agencia.endereco:
                    ET.SubElement(agencia_elem, 'endereco').text = str(agencia.endereco)
                if agencia.telefone:
                    ET.SubElement(agencia_elem, 'telefone').text = str(agencia.telefone)
                
                # Adiciona contas
                contas = agencia.contas.all()
                if contas.exists():
                    contas_elem = ET.SubElement(agencia_elem, 'contas')
                    
                    for conta in contas:
                        conta_elem = ET.SubElement(contas_elem, 'conta')
                        
                        ET.SubElement(conta_elem, 'numero').text = str(conta.numero)
                        ET.SubElement(conta_elem, 'tipo_conta').text = str(conta.tipo_conta)
                        ET.SubElement(conta_elem, 'saldo').text = str(conta.saldo)
                        ET.SubElement(conta_elem, 'ativa').text = 'true' if conta.ativa else 'false'
    
    # Converte para string com formatação
    xml_str = ET.tostring(root, encoding='unicode')
    
    # Formata o XML com indentação
    dom = ET.fromstring(xml_str)
    _indent(dom)
    xml_formatado = ET.tostring(dom, encoding='unicode')
    
    # Adiciona declaração XML
    return '<?xml version="1.0" encoding="UTF-8"?>\n' + xml_formatado


def _indent(elem, level=0):
    """Helper para formatar XML com indentação"""
    indent_str = "\n" + "  " * level
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = indent_str + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = indent_str
        for child in elem:
            _indent(child, level + 1)
        if not child.tail or not child.tail.strip():
            child.tail = indent_str
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = indent_str


def importar_bancos_xml(arquivo_xml):
    """
    Importa bancos, agências e contas bancárias de um arquivo XML.
    
    Formato esperado do XML:
    <bancos>
        <banco>
            <codigo>001</codigo>
            <nome>Banco do Brasil</nome>
            <descricao>Banco Estatal</descricao>
            <agencies>
                <agencia>
                    <numero>0001</numero>
                    <nome>Agência Centro</nome>
                    <endereco>Rua Principal, 100</endereco>
                    <telefone>(11) 1234-5678</telefone>
                    <contas>
                        <conta>
                            <numero>123456</numero>
                            <tipo_conta>corrente</tipo_conta>
                            <saldo>5000.00</saldo>
                            <ativa>true</ativa>
                        </conta>
                    </contas>
                </agencia>
            </agencies>
        </banco>
    </bancos>
    """
    
    try:
        if isinstance(arquivo_xml, str):
            root = ET.fromstring(arquivo_xml)
        else:
            root = ET.parse(arquivo_xml).getroot()
        
        resultado = {
            'bancos_criados': 0,
            'bancos_atualizados': 0,
            'agencias_criadas': 0,
            'agencias_atualizadas': 0,
            'contas_criadas': 0,
            'contas_atualizadas': 0,
            'erros': []
        }
        
        # Processa cada banco
        for banco_elem in root.findall('banco'):
            try:
                codigo = banco_elem.findtext('codigo', '').strip()
                nome = banco_elem.findtext('nome', '').strip()
                descricao = banco_elem.findtext('descricao', '').strip()
                
                if not codigo or not nome:
                    resultado['erros'].append('Banco sem código ou nome')
                    continue
                
                # Criar ou atualizar banco
                banco, created = Banco.objects.get_or_create(
                    codigo=codigo,
                    defaults={
                        'nome': nome,
                        'descricao': descricao
                    }
                )
                
                if created:
                    resultado['bancos_criados'] += 1
                else:
                    banco.nome = nome
                    banco.descricao = descricao
                    banco.save()
                    resultado['bancos_atualizados'] += 1
                
                # Processa agências
                agencias_elem = banco_elem.find('agencias')
                if agencias_elem is not None:
                    for agencia_elem in agencias_elem.findall('agencia'):
                        try:
                            ag_numero = agencia_elem.findtext('numero', '').strip()
                            ag_nome = agencia_elem.findtext('nome', '').strip()
                            ag_endereco = agencia_elem.findtext('endereco', '').strip()
                            ag_telefone = agencia_elem.findtext('telefone', '').strip()
                            
                            if not ag_numero or not ag_nome:
                                resultado['erros'].append(
                                    f'Agência do banco {codigo} sem número ou nome'
                                )
                                continue
                            
                            # Criar ou atualizar agência
                            agencia, created = Agencia.objects.get_or_create(
                                banco=banco,
                                numero=ag_numero,
                                defaults={
                                    'nome': ag_nome,
                                    'endereco': ag_endereco,
                                    'telefone': ag_telefone
                                }
                            )
                            
                            if created:
                                resultado['agencias_criadas'] += 1
                            else:
                                agencia.nome = ag_nome
                                agencia.endereco = ag_endereco
                                agencia.telefone = ag_telefone
                                agencia.save()
                                resultado['agencias_atualizadas'] += 1
                            
                            # Processa contas
                            contas_elem = agencia_elem.find('contas')
                            if contas_elem is not None:
                                for conta_elem in contas_elem.findall('conta'):
                                    try:
                                        c_numero = conta_elem.findtext('numero', '').strip()
                                        c_tipo = conta_elem.findtext('tipo_conta', 'corrente').strip()
                                        c_saldo = conta_elem.findtext('saldo', '0').strip()
                                        c_ativa = conta_elem.findtext('ativa', 'true').strip().lower() == 'true'
                                        
                                        if not c_numero:
                                            resultado['erros'].append(
                                                f'Conta da agência {ag_numero} sem número'
                                            )
                                            continue
                                        
                                        try:
                                            saldo = Decimal(c_saldo)
                                        except (ValueError, TypeError):
                                            saldo = Decimal('0')
                                        
                                        # Criar ou atualizar conta
                                        conta, created = ContaBancaria.objects.get_or_create(
                                            agencia=agencia,
                                            numero=c_numero,
                                            defaults={
                                                'tipo_conta': c_tipo,
                                                'saldo': saldo,
                                                'ativa': c_ativa
                                            }
                                        )
                                        
                                        if created:
                                            resultado['contas_criadas'] += 1
                                        else:
                                            conta.tipo_conta = c_tipo
                                            conta.saldo = saldo
                                            conta.ativa = c_ativa
                                            conta.save()
                                            resultado['contas_atualizadas'] += 1
                                    
                                    except Exception as e:
                                        resultado['erros'].append(
                                            f'Erro ao processar conta: {str(e)}'
                                        )
                        
                        except Exception as e:
                            resultado['erros'].append(
                                f'Erro ao processar agência: {str(e)}'
                            )
            
            except Exception as e:
                resultado['erros'].append(f'Erro ao processar banco: {str(e)}')
        
        return resultado
    
    except ET.ParseError as e:
        return {
            'bancos_criados': 0,
            'bancos_atualizados': 0,
            'agencias_criadas': 0,
            'agencias_atualizadas': 0,
            'contas_criadas': 0,
            'contas_atualizadas': 0,
            'erros': [f'Erro ao fazer parse do XML: {str(e)}']
        }
    except Exception as e:
        return {
            'bancos_criados': 0,
            'bancos_atualizados': 0,
            'agencias_criadas': 0,
            'agencias_atualizadas': 0,
            'contas_criadas': 0,
            'contas_atualizadas': 0,
            'erros': [f'Erro inesperado: {str(e)}']
        }
