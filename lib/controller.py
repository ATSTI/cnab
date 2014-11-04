# -*- encoding: utf-8 -*-
from time import gmtime, strftime

class CNAB400(object):

    def __init__(self,dic):
        self.banco = dic['codigo_banco']
        self.registro = ["cobranca_registrada"]
        self.dados = dic

    def processa_remessa(self):

        if self.banco == '399':

            if "cobranca_registrada" in self.registro:

                from CNAB_400.hsbc import cobranca_registrada

                string = ''

                arquivo = open('remessa.txt','w')

                #HEADER
                header = cobranca_registrada.Header(self.dados)
                header_linha = monta_linha(header.dados,header.campos)
                string += '%s' % header
                arquivo.write(header_linha.encode("ascii","ignore").upper())

                #DETALHE
                for d in self.dados['detalhes']:

                    detalhe = cobranca_registrada.Detalhe(d)
                    detalhe_linha = monta_linha(detalhe.dados,detalhe.campos)
                    string += '\n%s' % detalhe_linha

                    #raise Exception(len(detalhe_linha))
                    arquivo.write('\n' + detalhe_linha.encode("ascii","ignore").upper())
                    raise Exception(len(detalhe_linha))

                #TRAILER
                trailer = cobranca_registrada.Trailer(self.dados)
                trailer_linha = monta_linha(trailer.dados,trailer.campos)
                string += '\n%s' % trailer
                arquivo.write('\n' + trailer_linha.encode("ascii","ignore").upper())


                return string.encode("ascii","ignore")
                #raise Exception(arquivo.read())
                #return header_linha

class CNAB400Retorno(object):

    def __init__(self,banco):

        self.banco = banco

    def processa_retorno(self):

        if self.banco == '399':

            from CNAB_400.hsbc import cobranca_registrada

            header_linha = ''
            detalhe = []
            trailer = ''

            a = open('Scd1403l.rem','r')

            linhas = a.readlines()

            for l in linhas:

                if l[0:1] == '0':

                    header = []

                    p = 0

                    for h in cobranca_registrada.HeaderRetorno().campos:

                        header.append([str(h[0]),l[p:p+h[1]]])
                        p += h[1]


                if l[0:1] == '1':

                    p = 0
                    detalhe_item = []

                    for d in cobranca_registrada.DetalheRetorno().campos:
                        #raise Exception(d)
                        detalhe_item.append([str(d[0]),l[p:p+d[1]]])
                        p += d[1]
                    #raise Exception(detalhe_item)

                    detalhe.append(detalhe_item)



                if l[0:1] == '9':
                    trailer = l


            a.close()



            print #trailer
            #raise Exception(linhas)


def monta_linha(dados,lista_campos):

    linha = ''
    campos_vazios = []

    for c in lista_campos:

        # Captura campos com valores padrões
        if c[2] != None:

            item = c[2]
            l = len(u'%s'% c[2])

            if l < c[1]:
                raise Exception("Quantidade de caracteres para o campo '%s' menor que '%s' '%s'!" % (c[0],c[1],item))
                #item = item.ljust(c[1],' ')

            if l > c[1]:
                raise Exception("Quantidade de caracteres para o campo '%s' maior que '%s'!" % (c[0],c[1]))

            linha += u'%s' % item

        # Monta campos com espaço
        if c[2] == 's':
            item = ''
            item.ljust(c[1],' ')
            linha += item


        # Captura campos enviados no dicionário
        if c[2] == None and c[0] in dados:

            item = dados[c[0]]
            l = len(u'%s'% item)

            if l < c[1]:
                raise Exception("Quantidade de caracteres para o campo '%s' menor que '%s' '%s'!" % (c[0],c[1],item))
                #item = item.ljust(c[1],' ')

            if l > c[1]:
                raise Exception("Quantidade de caracteres para o campo '%s' maior que '%s'!" % (c[0],c[1]))

            linha += u'%s' % item

        if c[2] == None and not c[0] in dados:

            campos_vazios.append(c[0])

    if campos_vazios:
        raise Exception("Campo(s) %s são obrigatórios e não constam no dicionário!" % (campos_vazios))

    return linha
    #raise Exception(linha)

def campos_obrigatorios(lista_campos):
    campos = []
    for c in lista_campos:

        if c[2] == None:
            campos.append(c[0])
    return campos


