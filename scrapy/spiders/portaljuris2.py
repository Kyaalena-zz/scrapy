# scrapy crawl tjpr2

import scrapy
import re
import copy

class PortalTJPRScrapy(scrapy.Spider):
    name = 'tjpr2'
    url = ["https://portal.tjpr.jus.br/jurisprudencia/"]
    #meta_dict={}

    def start_requests(self):
        for u in self.url:
            yield scrapy.Request(u, callback=self.parse_cover)

    #hace el parseo de la portada de la búsqueda y lanza la búsqueda
    def parse_cover(self, response):    

        abspath_search_post = 'https://portal.tjpr.jus.br/jurisprudencia/publico/pesquisa.do?actionType=pesquisar'

        #ponemos los parámetros de la búsqueda que nos interesan
        form_custom_params = {
    'backURL': '',
    'selectedIcon': 'tabDetalhada',
    'pesquisaLivre': '',
    'postCampo': '',
    'tmp': '',
    'criterioPesquisa': '"Novo CPC"',
    'idLocalPesquisa': '1',
    'idClasseProcessual': '',
    'descricaoClasseProcessual': 'Digite...',
    'idAssunto': '',
    'descricaoAssunto': '',
    'idOrgaoJulgadorSelecao': '',
    'nomeOrgaoJulgador': 'Digite...',
    'idOrgaoJulgador': '',
    'idRelator': '',
    'nomeRelator': 'Digite...',
    'idComarca': '',
    'nomeComarca': 'Digite...',
    'processo': 'Digite...',
    'acordao': 'Digite...',
    'dataJulgamentoInicio': '03/10/2018',
    'dataJulgamentoFim': '03/10/2018',
    'dataPublicacaoInicio': '',
    'dataPublicacaoFim': '',
    'idsTipoDecisaoSelecionados': '1',
    'mostrarCompleto': 'true',
    # 'ambito': '4',
    # 'ambito': '6',
    'ambitoDesc': '4,6',
    'pageSize': '10',
    # PAGINADO donde estoy 
    'page': '1',
    # PAGINADO la que quiero cargar 
    'pageNumber':'1',
    'sortColumn': 'processo_dataJulgamento',
    'sortOrder': 'DESC',
    'pageVoltar': '',
    # 'ambitoDesc': '4,6'
    }
        
        meta_dict = {}

        meta_dict['form_params'] = form_custom_params
        meta_dict['abspath_search_post']=abspath_search_post

        #Lanza la busqueda con el form
        return scrapy.FormRequest(
            url=abspath_search_post, 
            headers={}, 
            formdata= form_custom_params, 
            meta=meta_dict, 
            errback=self.errback_log,
            callback=self.parse_serp
        )

    def parse_serp(self, response):

        #XPATHS
        x_path_info_resultados = 'string(//*[@id="navigator"]/div[2])'
        x_path_paginado = '//*/div[@class="navRight"]/b/text()'
        x_path_listado_documentos = '//table[@class="resultTable linksacizentados juris-dados-completos"]'
        x_path_resultado_in_tabla_resultados_ficha_datos = './/*/tr[@class="even" or @class="odd"]'
        x_path_resultado_in_tabla_resultados_ficha_datos_tipo_fila = './/*/b/text()'
        x_path_resultado_in_tabla_resultados_ficha_datos_contenido_ementa = './/div[contains(@id,"ementa")]'
        x_path_resultado_in_tabla_resultados_ficha_datos_contenido_integra = './/div[contains(@id,"texto")]'
        x_path_resultado_in_tabla_resultados_ficha_datos_descarga_zip = 'string(.//a[contains(@href, "/jurisprudencia/publico/visualizacao.do")]/@href)'
        x_path_pag_siguiente = '//*[@id="navigator"]/div[1]/a[@class="arrowNextOn"]/@href'
        x_path_pag_ultima = '//*[@id="navigator"]/div[1]/a[@class="arrowLastOn"]/@href'
      
        #EXPRESIONES REGULARES
        regexp_processo = r"Processo:\s+(?P<nproceso>[\d\.-]+)\s+\((?P<tipo>.*)\)"
        regexp_segredo = r"Segredo de Justiça:\s+(?P<segredo>.*)"
        regexp_relator = r"Relator\(a\):\s+(?P<relator>.*)"
        regexp_organo = r"Órgão Julgador:\s+(?P<organo>.*)"
        regexp_comarca = r"Comarca:\s+(?P<comarca>.*)"
        regexp_fecha_julgamento = r"Julgamento:\s+(?P<fecha_julgamento>\d{1,2}\/\d{1,2}\/\d{2,4})"
        regexp_fecha_publicacion = r"Publicação:\s+(?P<fecha_publicacion>\d{1,2}\/\d{1,2}\/\d{2,4})"
        regexp_fecha_zip = r"javascript:document\.location\.replace\('(?P<urlzip>.*)'\);"
        regexp_paginado = r"forms\['pesquisaForm'\]\['(?P<key>.+?)'\]\.value='(?P<value>.+?)'"
        regexp_nregistros = r"(?P<nregistros>\d{1,})*.registro\(s\) encontrado\(s\),\s+exibindo de\s+(?P<ndocumentosporpag>.*)"
        regexp_ultimapagina = r"\['pageNumber'\]\.value='(?P<value>.\d{0,})"

         # IDENTIFICA_LINEAS = {
        #     'regexp_processo':  { 're': r"Processo:\s+(?P<nproceso>[\d\.-]+)\s+\((?P<tipo>.*)\)" },
        #     # 'relator': '',
        #     # 'organo': '',
        #     'regexp_fecha_en_texto':  r"Julgamento:\s+(?P<fecha>\d{1,2}\/\d{1,2}\/\d{2,4})",
        # }  
        #Registros y N exibición por pag
        numero_registros = None
        exibiendo = None
        n_resultados = response.xpath(x_path_info_resultados).extract_first()
        # print("Registros y N exibición por pag: __{}__".format(n_resultados))
        # print("..................................................................")
        match_registros = re.search(regexp_nregistros, n_resultados, re.MULTILINE | re.IGNORECASE | re.UNICODE )
        #print(match_registros)
        # for registro in match_registros:
        #     print("Numero: __{}__ N exibición por pag: __{}__".format(registro[0],registro[1]))
        #     print("."*66) 

        numero_registros = match_registros.groupdict().get('nregistros', None)
        exibiendo = match_registros.groupdict().get('ndocumentosporpag', None)
        # print("Numero: __{}__ N exibición por pag: __{}__".format(numero_registros,exibiendo))
        # print("."*66)
        print(numero_registros)

        if int(numero_registros) == 0:
            print("En esta busqueda NO HAY REGISTROS")
        else:
            print("si hay registros")

            meta_dict = copy.deepcopy(response.meta)

            #página siguiente
            str_pagina_siguiente = response.xpath(x_path_pag_siguiente).extract_first()
            # print("Paginado: __{}__".format(str_pagina_siguiente))
            # print("."*66)        
            
            params_pagina_siguiente = {}
            match_pagina_siguiente = re.findall(regexp_paginado, str_pagina_siguiente, re.MULTILINE | re.IGNORECASE | re.UNICODE ) if str_pagina_siguiente else []
            for paginado in match_pagina_siguiente:
                #print("key: __{}__  Value: __{}__".format(paginado[0],paginado[1]))
                #print("."*66)
                params_pagina_siguiente[paginado[0]] = paginado[1]


            #última página
            str_pagina_ultima = response.xpath(x_path_pag_ultima).extract_first()
            # print("Paginado: __{}__".format(str_pagina_ultima))
            # print("."*66)        

            params_pagina_ultima = {}
            match_pagina_ultima = re.findall(regexp_paginado, str_pagina_ultima, re.MULTILINE | re.IGNORECASE | re.UNICODE ) if str_pagina_ultima else []
            for paginado in match_pagina_ultima:
                # print("key: __{}__  Value: __{}__".format(paginado[0],paginado[1]))
                # print("."*66)
                params_pagina_ultima[paginado[0]] = paginado[1]

            print("Página actual: {} Página siguiente: {} Última: {}".format(
                meta_dict.get('form_params',{}).get('pageNumber',0),
                params_pagina_siguiente.get('pageNumber',0),
                params_pagina_ultima.get('pageNumber',0)
            ))


            if int(params_pagina_siguiente.get('pageNumber',0)) <= int(params_pagina_ultima.get('pageNumber',0)):

                meta_dict.get('form_params',{}).update({
                    'pageNumber': str(int(meta_dict.get('form_params',{}).get('pageNumber',0))+1)
                })

                print("\n\nVOY A PEDIR LA pÄGINA: {}\n\n".format(meta_dict.get('form_params',{}).get('pageNumber',0)))
                #Lanza la busqueda con el form
                yield scrapy.FormRequest(
                    url=meta_dict.get('abspath_search_post'), 
                    headers={}, 
                    formdata= meta_dict.get('form_params',{}), 
                    meta=meta_dict, 
                    errback=self.errback_log,
                    callback=self.parse_serp
                )

            # Numero de Pag actual
            # paginado = response.xpath(x_path_paginado).extract_first()
            # int(paginado)
            # print("PAGINA: __{}__".format(paginado))
            # print("."*66)
            
            lista_resultados = response.xpath(x_path_listado_documentos)
            # tabla_resultados = response.xpath(x_path_tabla_resultados)
            # print("TABLA RESULTADOS: __{}__".format(tabla_resultados))
            # print("..................................................................")

            # resultado_en_resultados = tabla_resultados.xpath(x_path_resultado_in_tabla_resultados)
            # print("RESULTADOS {}: __{}__".format(len(resultado_en_resultados), resultado_en_resultados))
            # print("."*66)

            for i,resultado in enumerate(lista_resultados):
    
                print("..................................................................")
                print("N DOCUMENTO: __{}__".format(i+1))
                #atributos de ficha 
                numero_proceso = None
                segredo = None
                relator = None
                organo = None
                comarca = None
                fecha_julgamento = None
                fecha_publicacion = None
                tipo_proceso = None
                ementa = None
                integra = None
                archivo_zip = None

                for fila in resultado.xpath(x_path_resultado_in_tabla_resultados_ficha_datos):
                
                    linea_cleaned = fila.xpath('string(.)').extract_first()
                    tipo_linea = fila.xpath(x_path_resultado_in_tabla_resultados_ficha_datos_tipo_fila).extract_first()   
                    
                    #print("Tipo de linea: _{}_".format(tipo_linea))
                    #print(linea_cleaned[:300])
                    if tipo_linea and 'EMENTA' in tipo_linea.upper().strip():
                        ementa = fila.xpath(x_path_resultado_in_tabla_resultados_ficha_datos_contenido_ementa).extract()
                        #print("__Ementa: {}".format(ementa[:5]))
                        continue

                    if tipo_linea and ( 'ÍNTEGRA' in tipo_linea.upper().strip() or 'INTEGRA' in tipo_linea.upper().strip() ):
                        integra = fila.xpath(x_path_resultado_in_tabla_resultados_ficha_datos_contenido_integra).extract_first()
                        #print("__Integra: {}".format(integra[:30]))
                        continue

                    #Descarga de archivo zip 
                    if not tipo_linea:
                        archivo_zip_js_link = fila.xpath(x_path_resultado_in_tabla_resultados_ficha_datos_descarga_zip).extract_first()
                        match_url_zip = re.search(regexp_fecha_zip, archivo_zip_js_link,  re.MULTILINE | re.IGNORECASE | re.UNICODE )
                        #print(match_url_zip)
                        if match_url_zip:
                            archivo_zip = match_url_zip.groupdict().get('urlzip', None)

                    #proceso
                    match_proceso = re.search(regexp_processo, linea_cleaned, re.MULTILINE | re.IGNORECASE | re.UNICODE )
                    if match_proceso:
                        numero_proceso = match_proceso.groupdict().get('nproceso', None)
                        tipo_proceso = match_proceso.groupdict().get('tipo', None)
                        continue

                    #segredo
                    match_segredo = re.search(regexp_segredo, linea_cleaned,  re.MULTILINE | re.IGNORECASE | re.UNICODE )
                    if match_segredo:
                        segredo = match_segredo.groupdict().get('segredo', None)
                        continue

                    #relator
                    match_relator = re.search(regexp_relator, linea_cleaned,  re.MULTILINE | re.IGNORECASE | re.UNICODE )
                    if match_relator:
                        relator = match_relator.groupdict().get('relator', None)
                        continue

                    #organo julgador
                    match_organo = re.search(regexp_organo, linea_cleaned,  re.MULTILINE | re.IGNORECASE | re.UNICODE )
                    if match_organo:
                        organo = match_organo.groupdict().get('organo', None)
                        continue

                    #comarca
                    match_comarca = re.search(regexp_comarca, linea_cleaned,  re.MULTILINE | re.IGNORECASE | re.UNICODE )
                    if match_comarca:
                        comarca = match_comarca.groupdict().get('comarca', None)
                        continue
                
                    #fecha julgamento
                    match_fecha_julgamento = re.search(regexp_fecha_julgamento, linea_cleaned,  re.MULTILINE | re.IGNORECASE | re.UNICODE )
                    if match_fecha_julgamento:
                        fecha_julgamento = match_fecha_julgamento.groupdict().get('fecha_julgamento', None)
                        continue

                    #Fonte/Data da Publicação
                    match_fecha_publicacion = re.search(regexp_fecha_publicacion, linea_cleaned,  re.MULTILINE | re.IGNORECASE | re.UNICODE )
                    if match_fecha_publicacion:
                        fecha_publicacion = match_fecha_publicacion.groupdict().get('fecha_publicacion', None)
                        continue

                print("Info documento:\n __Número Processo:{}\n __Segredo de Justiça:{}\n __Relator(a):{}\n __Órgão Julgador:{}\n __Comarca:{}\n __Tipo:{}\n __Data do Julgamento:{}\n __Data da Publicação:{}\n __Ementa:{}\n __Integra:{}\n  __Carregar documento:{}"
                .format(
                    numero_proceso,
                    segredo,
                    relator[:100],
                    organo,
                    comarca,
                    tipo_proceso,
                    fecha_julgamento,
                    fecha_publicacion if fecha_publicacion else 'VACIO',
                    ementa[:10],
                    integra[:10],
                    response.urljoin(archivo_zip)
                    
                ))

                if archivo_zip:
                    #print("AHORA VOY POR EL ZIP DEL PROCESO {} CON URL: \n{}".format(numero_proceso,archivo_zip))
                    yield scrapy.Request(response.urljoin(archivo_zip), callback=self.parse_nothing)
                
                #print("__Archivo Zip: {}".format(archivo_zip))
                    # tipo_fila = fila.xpath(x_path_resultado_in_tabla_resultados_ficha_datos_tipo_fila).extract_first()
                    # if tipo_fila and ( tipo_fila.strip().upper() not in ['Ementa'.upper(), 'Íntegra do Acórdão'.upper(), 'Integra do Acórdão'.upper()] ):
                    #     linea_cleaned = fila.xpath('string(.)').extract_first()
                    #     if len(linea_cleaned.split(':'))>1:
                    #         print(linea_cleaned.split(':')[0].strip())
                    #         print(linea_cleaned.split(':')[1].strip())

    def parse_nothing(self, response):
        print("{}\n\nSoy la URL: \n{}".format("."*60,response.url))
        
    def errback_log(self, failure):
        # log all failures
        response = failure.value.response
        request = response.request
        self.logger.error("--RESPONSE--")
        self.logger.error(response.url)
        self.logger.error("-- failure --")
        self.logger.error(repr(failure))
        self.logger.error("-- response.body --")
        self.logger.error(request.body)
        self.logger.error("--")
        self.logger.error("--REQUEST--")
        self.logger.error(request.meta)
        self.logger.error("--")
        self.logger.error(request.headers)
        self.logger.error("--")
        self.logger.error(request.body)
        self.logger.error("--")

