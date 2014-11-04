# -*- encoding: utf-8 -*-

#ARQUIVO REMESSA
class Header(object):

    def __init__(self,dic):

        self.dados = None

        if 'header' in dic:
            self.dados = dic['header']
        else:
            raise Exception('Registro "Header" não consta no dicionário!')

        self.campos = [
            ['codigo_registro',1,'0'],
            ['codigo_arquivo',1,'1'],
            ['literal_arquivo',7,'REMESSA'],
            ['codigo_servico',2,'01'],
            ['literal_servico',15,'COBRANCA'.ljust(15,' ')],
            ['zero',1,'0'],
            ['agencia_cedente',4,None],
            ['sub_conta',2,'55'],
            ['conta_corrente',11,None],
            ['banco',2,''.ljust(2,' ')],
            ['nome_cliente',30,None],
            ['codigo_banco',3,'399'],
            ['nome_banco',15,'HSBC'.ljust(15,' ')],
            ['data_gravacao',6,None],
            ['densidade',5,'01600'],
            ['literal_densidade',3,'BPI'],
            ['banco',2,''.ljust(2,' ')],
            ['sigla_layout',7,'LANCV08'],
            ['banco',277,''.ljust(277,' ')],
            ['numero_sequencial',6,None],
        ]

class Detalhe(object):

    def __init__(self,dic):

        self.dados = None

        if 'detalhe' in dic:
            self.dados = dic['detalhe']
        else:
            raise Exception('Registro "Detalhe" não consta no dicionário!')

        self.campos = [
            ['codigo_registro',1,'1'],
            ['codigo_inscricao',2,None],
            ['numero_inscricao',14,None],
            ['zero',1,'0'],
            ['agencia_cedente',4,None],
            ['sub_conta',2,'55'],
            ['conta_corrente',11,None],
            ['brancos',2,''.ljust(2,' ')],
            ['controle_participante',25,None],
            ['nosso_numero',11,None],
            ['desconto_data_2',6,None],
            ['valor_desconto_2',9,None],
            ['desconto_data_3',6,None],
            ['valor_desconto_3',9,None],
            ['carteira',1,None],
            ['codigo_ocorrencia',2,None],
            ['seu_numero',10,None],
            ['vencimento',6,None],
            ['valor_titulo',13,None],
            ['banco_cobrador',3,'399'],
            ['agencia_depositaria',5,'00000'],
            ['especie',2,None],
            ['aceite',1,None],
            ['data_emissao',6,None],
            ['instrucao_1',2,None],
            ['instrucao_2',2,None],
            ['juros_mora',13,None],
            ['desconto_data',6,None],
            ['valor_desconto',13,None],
            ['valor_IOF',11,None],
            ['valor_abatimento',11,None],
            ['codigo_inscricao_pagador',2,None],
            ['numero_inscricao_pagador',14,None],
            ['nome_pagador',40,None],
            ['endereco_pagador',38,None],
            ['inst_nao_receb_boleto',2,None],
            ['bairro_pagador',12,None],
            ['cep_pagador',5,None],
            ['sufixo_cep_pagador',3,None],
            ['cidade_pagador',15,None],
            ['sigla_UF',2,None],
            ['sacador_avalista',39,None],
            ['tipo_boleto',1,None],
            ['prazo_protesto',2,None],
            ['moeda',1,None],
            ['numero_sequencial',6,None],
        ]

class Trailer(object):

    def __init__(self,dic):

        self.dados = None

        if 'trailer' in dic:
            self.dados = dic['trailer']
        else:
            raise Exception('Registro "Trailer" não consta no dicionário!')

        self.campos = [
            ['codigo_registro',1,'9'],
            ['banco',393,' '],
            ['numero_sequencial',6,None]

        ]

#ARQUIVO RETORNO
class HeaderRetorno(object):

    def __init__(self):

        self.campos = [
            ['codigo_registro',1,'0'],
            ['codigo_arquivo',1,'1'],
            ['literal_arquivo',7,'REMESSA'],
            ['codigo_servico',2,'01'],
            ['literal_servico',15,'COBRANCA'],
            ['zero',1,'0'],
            ['agencia_cedente',4,None],
            ['sub_conta',2,None],
            ['conta_corrente',11,None],
            ['banco',2,'s'],
            ['nome_cliente',30,None],
            ['codigo_banco',3,'399'],
            ['nome_banco',15,'HSBC'],
            ['data_gravacao',6,None],
            ['densidade',5,'01600'],
            ['literal_densidade',3,'BPI'],
            ['banco',11,'s'],
            ['data_credito',6,None],
            ['banco',263,'s'],
            ['sequencial_arquivo',5,None],
            ['banco',1,None],
            ['numero_sequencial',6,None],
        ]

class DetalheRetorno(object):

    def __init__(self):

        self.campos = [
            ['codigo_registro',1,'1'],
            ['codigo_inscricao',2,None],
            ['numero_incricao',14,None],
            ['zero',1,'0'],
            ['agencia_cedente',4,None],
            ['sub_conta',2,'55'],
            ['conta_corrente',11,None],
            ['origem_pagamento',1,None],
            ['banco',1,'s'],
            ['controle_participante',25,None],
            ['nosso_numero',11,None],
            ['desconto_data_2',6,None],
            ['valor_desconto_2',11,None],
            ['desconto_data_3',6,None],
            ['valor_desconto_3',11,None],
            ['carteira',1,None],
            ['codigo_ocorrencia',2,None],
            ['data_ocorrencia',6,None],
            ['seu_numero',10,None],
            ['nosso_numero',11,None],
            ['banco',9,None],
            ['vencimento',6,None],
            ['valor_titulo',13,None],
            ['banco_cobrador',3,'399'],
            ['agencia_cobradora',5,None],
            ['especie',2,None],
            ['tarifa_custas',11,None],
            ['banco',39,None],
            ['valor_abatimento',11,None],
            ['valor_desconto',11,None],
            ['valor_pago',11,None],
            ['juros_mora',11,None],
            ['banco',22,None],
            ['complemento_ocorrencia',2,None],
            ['indicativo_credito',1,None],
            ['banco',84,None],
            ['numero_aviso',5,None],
            ['tipo_moeda',1,None],
            ['numero_sequencial',6,None]
        ]


class TrailerRetorno(object):

    def __init__(self,dic):

        self.dados = None

        if 'trailer' in dic:
            self.dados = dic['trailer']
        else:
            raise Exception('Registro "Trailer" não consta no dicionário!')

        self.campos = [
            ['codigo_registro',1,None],
            ['codigo_arquivo',1,None],
            ['codigo_servico',2,None],
            ['codigo_banco',3,None],
            ['banco',10,'s'],
            ['quantidade_ser',8,None],
            ['valor_ser',12,None],
            ['banco',355,None],
            ['numero_sequencial',6,None]

        ]