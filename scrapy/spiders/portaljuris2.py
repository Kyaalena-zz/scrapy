# scrapy crawl tjpr2

import scrapy

class PortalTJPRScrapy(scrapy.Spider):
    name = 'tjpr2'
    url = ["https://portal.tjpr.jus.br/jurisprudencia/"]
    

    def start_requests(self):
        for u in self.url:
            yield scrapy.Request(u, callback=self.parse_cover)

    #hace el parseo de la portada de la búsqueda y lanza la búsqueda
    def parse_cover(self, response):      
        #ponemos los parámetros de la búsqueda que nos interesan
        form_custom_params = {
            'criterioPesquisa': 'novo cpc',
            'mostrarCompleto' : 'true'
        }

        submit_form = scrapy.FormRequest.from_response(response, formxpath='//*[@id="pesquisaForm"]', 
        formdata=form_custom_params, clickdata='Pesquisar',  callback=self.parse_serp)
        yield submit_form


    # def parse(self, response):
    #     print(response)

    def parse_serp(self, response):

        #XPATHS
        x_path_paginado = '//*[@id="navigator"]/div[1]'
        x_path_info_resultados = 'string(//*[@id="navigator"]/div[2])'
        x_path_tabla_resultados = './/*[@class="juris-parametros"]'
        x_path_resultado_in_tabla_resultados = './/*[@class="resultTable jurisprudencia semborda"]'
        x_path_resultado_in_tabla_resultados_num_documento = 'string(.//*[@class="resultTable jurisprudencia semborda"])'
        x_path_resultado_in_tabla_resultados_ficha = './/*[@class="resultTable linksacizentados juris-dados-completos"]' 
        x_path_resultado_in_tabla_resultados_ficha_datos = './/*/tr[@class="even" or @class="odd"]'
        
        
        x_path_resultado_in_tabla_resultados_ficha_datos_processo = 'string(.//*[@id="pesquisaForm"]//table[2]//tr[2])'
        x_path_resultado_in_tabla_resultados_ficha_datos_segredo = 'string(.//*[@id="pesquisaForm"]//td//tr[3]/td)'


        #xpath para scrapig de forma 2 
        
        x_path_resultado_in_tabla_resultados_ficha_link_detalle = './a/@href'
        x_path_resultado_in_tabla_resultados_ficha_num_proceso = './a/text()'
        x_path_resultado_in_tabla_resultados_ficha_misc = './text()'
        x_path_resultado_in_tabla_resultados_ficha_decisao = './/*[@class="decisao"]/text()'
        x_path_resultado_in_tabla_resultados_resumen = './td[@class="juris-tabela-ementa"]'  

       
        #EXPRESIONES REGULARES
        regexp_parseo_n_resultados = r"(?P<nresultados>\d+?)\s+.*?(?P<pag>\d+)\s+.*?(?P<pag_total>\d+)"
        regexp_fecha_en_texto = regex = r"(?P<fecha>\d{1,2}\/\d{1,2}\/\d{2,4})"

        n_resultados = response.xpath(x_path_info_resultados).extract_first()
        print("N Resultados: __{}__".format(n_resultados))
        print("..................................................................")

        paginado = response.xpath(x_path_paginado).extract_first()
        print("PAGINADO: __{}__".format(paginado))
        print("..................................................................")

        tabla_resultados = response.xpath(x_path_tabla_resultados)
        print("TABLA RESULTADOS: __{}__".format(tabla_resultados))
        print("..................................................................")

        resultado_en_resultados = tabla_resultados.xpath(x_path_resultado_in_tabla_resultados)
        print("RESULTADOS {}: __{}__".format(len(resultado_en_resultados), resultado_en_resultados))
        print("..................................................................")


        #for i,resultado in enumerate(resultado_en_resultados):

        ficha = response.xpath(x_path_resultado_in_tabla_resultados_ficha)
        # print(ficha)
        # print("..................................................................")

        for fichas in ficha:
            num_doc = response.xpath(x_path_resultado_in_tabla_resultados_num_documento).extract_first()
            print("N DOCUMENTO: __{}__".format(num_doc))
            print("..................................................................")

            filas =  response.xpath(x_path_resultado_in_tabla_resultados_ficha_datos).extract()
            #print(filas)

            for fila in [ ln.strip() for ln in filas if len(ln.strip()) > 0 ]:
                print("{}".format(fila))
                
        # num_proceso = ficha.xpath(x_path_resultado_in_tabla_resultados_ficha_num_proceso).extract_first()
        # print("NUM PROCESO: __{}__".format(num_proceso.strip()))
        # print("..................................................................")

        # link = ficha.xpath(x_path_resultado_in_tabla_resultados_ficha_link_detalle).extract_first()
        # print("LINK A DETALLE: __{}__".format(link))
        # print("..................................................................")

        # decisao = ficha.xpath(x_path_resultado_in_tabla_resultados_ficha_decisao).extract_first()
        # print("TIPO DE DECISAO: __{}__".format(decisao))
        # print("..................................................................")
        
        # resumen = resultado.xpath(x_path_resultado_in_tabla_resultados_resumen)
        # print("RESUMEN: __{}__".format(resumen))

        # # print("RESULTADO: {}".format(i))
        # ficha = resultado.xpath(x_path_resultado_in_tabla_resultados_ficha)
        # ficha_txt = ficha.xpath(x_path_resultado_in_tabla_resultados_ficha_misc).extract()
            
        # print("FICHA: __{}__".format(ficha_txt))

        # for linea_cleaned in [ ln.strip() for ln in ficha_txt if len(ln.strip()) > 0 ]:
                
        #     print("LINEA: {}".format(linea_cleaned))

        #     if "RELATOR" in linea_cleaned.upper():
        #         print("Soy relator!")
        #         print(linea_cleaned.split(':')[1].strip())    
        #     elif "PUBLICAÇÃO" in linea_cleaned.upper():
        #         print("Soy fecha de publicación!")
        #         print(linea_cleaned.split(':')[1].strip())
        #     elif "JULGADOR" in linea_cleaned.upper():
        #         print("Soy organo julgadr!")
        #         print(linea_cleaned.split(':')[1].strip())
        #     elif "JULGAMENTO" in linea_cleaned.upper():
        #         print("Soy fecha de julgamento!")
        #         print(linea_cleaned.split(':')[1].strip())
        
        # resultado_en_resultados = tabla_resultados.xpath(x_path_resultado_in_tabla_resultados)
        # print("RESULTADOS {}: __{}__".format(len(resultado_en_resultados), resultado_en_resultados))
        # print("..................................................................")