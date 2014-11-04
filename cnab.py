# -*- coding: utf-8 -*-
import logging
import datetime
from dateutil.relativedelta import relativedelta
from operator import itemgetter
import time
import openerp
from openerp import pooler, tools
from openerp.osv import fields, osv, expression
from openerp.tools.translate import _
from lib import controller as cnab
from time import gmtime, strftime
import json
from dateutil import parser


class cnab_cnab(osv.osv):
    _rec_name = 'ref'
    _name = "cnab.cnab"
    _columns = {
        'registros': fields.one2many('cnab.registro','cnab_id',string='Registros', required=True),
        'data_criacao': fields.datetime('Data de Criação',readonly=True),
        'state': fields.selection([('draft','Rascunho'), ('done','Lançado')], 'Status', readonly=True),
        'ref': fields.char('Referência',required=True),
        'empresa': fields.many2one('res.company','Empresa',required=True),
        'conta': fields.many2one('res.partner.bank','Conta Bancária',required=True),
        'lote':fields.many2one('cnab.lote','Lote',required=True)
    }

    _defaults = {
        'data_criacao': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'ref': lambda self,cr,uid,context={}: self.pool.get('ir.sequence').get(cr, uid, 'cnab.cnab'),
        'state': 'draft',
    }

    def create(self,cr,uid,vals,context=None):

        if not vals['registros']:
            raise osv.except_osv(_('Atenção!'), _('Você deve inserir pelo menos um registro para estre CNAB!'))
        else:
            registros = []

            for i in vals['registros']:
                i[2]['numero'] = i[2]['fatura']

                registros.append(i)

            vals['registros'] = registros

            return super(cnab_cnab, self).create(cr, uid, vals, context)


    def gera_arquivo(self,cr,uid,ids,context=None):

        dic = {}

        qtd_registros = 1

        for i in self.browse(cr,uid,ids):

            dic.update({
                'codigo_banco':i.conta.bank_bic,
                'header':{
                    'agencia_cedente':i.conta.bra_number,
                    'conta_corrente': str(i.conta.bra_number) + str(i.conta.acc_number) + str(i.conta.acc_number_dig),
                    'nome_cliente':i.conta.partner_id.legal_name[0:30],
                    'data_gravacao': strftime("%d%m%y", gmtime()),
                    'numero_sequencial': '000001',
                }
            })

            if i.registros:
                dic.update({'detalhes':[]})

                for f in i.registros:

                    dic['detalhes'].append({'detalhe':{
                        'r_codigo_registro': '1',
                        'codigo_inscricao': i.conta.cnab_codigo_inscricao,
                        'numero_inscricao': i.conta.cnab_numero_inscricao,
                        'r_zero':'0',
                        'agencia_cedente': i.conta.bra_number,
                        'r_sub_conta':'55',
                        'conta_corrente': str(i.conta.bra_number) + str(i.conta.acc_number) + str(i.conta.acc_number_dig),
                        'brancos':'  ',
                        'controle_participante': str(f.fatura.id).ljust(25,' '),
                        'nosso_numero': '00000000000',
                        'desconto_data_2': '000000',
                        'valor_desconto_2': '000000000',
                        'desconto_data_3': '000000',
                        'valor_desconto_3': '000000000',
                        'carteira':i.conta.cnab_carteira,
                        'codigo_ocorrencia':'01',
                        'seu_numero':str(f.fatura.id).rjust(10,' '),
                        'vencimento': parser.parse(f.fatura.date_due).strftime("%d%m%y"),
                        'valor_titulo': ("%.2f" % f.fatura.amount_total).replace('.','').rjust(13,'0'),
                        'r_banco_cobrador':'399',
                        'r_agencia_depositaria':'00000',
                        'especie':'09',
                        'aceite': 'N',
                        'data_emissao': strftime("%d%m%y", gmtime()),
                        'instrucao_1': '74',
                        'instrucao_2': '77',
                        'juros_mora': ("%.2f" % ((f.fatura.amount_total / 100) * f.juros_mora)).replace('.','').rjust(13,'0'),
                        'desconto_data':'000000',
                        'valor_desconto':'0000000000000',
                        'valor_IOF':'00000000000',
                        'valor_abatimento':'00000000000',
                        'r_codigo_inscricao_pagador':'00',
                        'r_numero_inscricao_pagador':'11111111111111',
                        'nome_pagador':f.fatura.partner_id.name.ljust(40,' '),
                        'endereco_pagador': str('%s %s' % (f.fatura.partner_id.street,f.fatura.partner_id.number)).ljust(38,' '),
                        'inst_nao_receb_boleto':'  ',
                        'bairro_pagador':f.fatura.partner_id.district.ljust(12,' '),
                        'cep_pagador':f.fatura.partner_id.zip[0:5],
                        'sufixo_cep_pagador':f.fatura.partner_id.zip[6:10],
                        'cidade_pagador':f.fatura.partner_id.l10n_br_city_id.name.ljust(15,' '),
                        'sigla_UF':f.fatura.partner_id.state_id.code,
                        'sacador_avalista':''.ljust(39,' '),
                        'tipo_boleto':i.conta.cnab_tipo_boleto,
                        'prazo_protesto':i.conta.cnab_prazo_protesto,
                        'moeda':'9',
                        'numero_sequencial':str(qtd_registros + 1).rjust(6,'0')
                    }})
                    qtd_registros += 1

            dic.update({ 'trailer':{
                'numero_sequencial': str(qtd_registros + 1).rjust(6,'0'),
            }})

        string = ''

        contador = 0
        #raise osv.except_osv(_('Atenção!'), _(dic['detalhes'][0]))

        for k,v in dic['detalhes'][0]['detalhe'].items():
            string += v
            contador += 1
            if contador == 9:
                raise osv.except_osv(_('Atenção!'), _(string))





        raise osv.except_osv(_('Atenção!'), _(len(string)))

        arquivo = cnab.CNAB400(dic).processa_remessa()
        raise osv.except_osv(_('Atenção!'), _(arquivo))


class cnab_registro(osv.osv):
    _rec_name = 'numero'
    _name = "cnab.registro"
    _columns = {
        'numero': fields.char('Número Sequencial',readonly=True),
        'fatura': fields.many2one('account.invoice','Fatura',required=True),
        'data_criacao': fields.datetime('Data de Criação',readonly=True),
        'cnab_id': fields.many2one('cnab.cnab','CNAB'),
        'juros_mora': fields.float('Juros %',digits=(12,2)),

    }
    _defaults = {
        'data_criacao': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    }

class cnab_lote(osv.osv):

    _rec_name = 'nome'
    _name = 'cnab.lote'
    _columns = {
        'nome': fields.char('Nome',required=True),
        'codigo_tipo': fields.char('Código Tipo',required=True),
    }

class res_partner_bank(osv.osv):
    _inherit = "res.partner.bank"
    _columns = {
        'cnab_codigo_inscricao': fields.char('Código Inscrição',size=2),
        'cnab_numero_inscricao': fields.char('Numero da Inscricão',size=14),
        'cnab_carteira': fields.char('Carteira',size=1),
        'cnab_tipo_boleto': fields.char('Tipo de Boleto',size=1),
        'cnab_prazo_protesto': fields.char('Prazo para Protesto',size=2)
    }

    _defaults = {
        'cnab_tipo_boleto': 'S'
    }