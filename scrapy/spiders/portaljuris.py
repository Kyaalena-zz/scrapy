# scrapy crawl tjpr

import scrapy

class PortalTJPRScrapy(scrapy.Spider):
    name = 'tjpr'
    url = ["https://portal.tjpr.jus.br/jurisprudencia/"]

    def start_requests(self):
        for u in self.url:
            yield scrapy.Request(u, callback=self.parse_cover)

    #hace el parseo de la portada de la búsqueda y lanza la búsqueda
    def parse_cover(self, response):      
        #ponemos los parámetros de la búsqueda que nos interesan
        form_custom_params = {
            'criterioPesquisa': 'novo cpc'
        }

        submit_form = scrapy.FormRequest.from_response(response, formxpath='//*[@id="pesquisaForm"]', 
        formdata=form_custom_params, clickdata='Pesquisar',  callback=self.parse_serp)
        yield submit_form


    def parse_serp(self, response):

        #XPATHS
        x_path_info_resultados = 'string(//*[@id="navigator"]/div[2])'
        x_path_paginado = '//*[@id="navigator"]/div[1]'
        x_path_tabla_resultados = '//*/table[@class="resultTable jurisprudencia"]'
        x_path_resultado_in_tabla_resultados = './/*/tr[@class="even" or @class="odd"]' 
        x_path_resultado_in_tabla_resultados_ficha = './td[@class="juris-tabela-dados"]/div[@class="juris-tabela-propriedades"]' 
        x_path_resultado_in_tabla_resultados_ficha_link_detalle = './a/@href'
        x_path_resultado_in_tabla_resultados_ficha_num_proceso = './a/text()'
        x_path_resultado_in_tabla_resultados_ficha_misc = './text()'
        x_path_resultado_in_tabla_resultados_ficha_decisao = './/*[@class="decisao"]/text()'
        x_path_resultado_in_tabla_resultados_resumen = './td[@class="juris-tabela-ementa"]'  

       
        #EXPRESIONES REGULARES
        regexp_parseo_n_resultados = r"(?P<nresultados>\d+?)\s+.*?(?P<pag>\d+)\s+.*?(?P<pag_total>\d+)"
        regexp_fecha_en_texto = regex = r"(?P<fecha>\d{1,2}\/\d{1,2}\/\d{2,4})"

        n_resultados = response.xpath(x_path_info_resultados).extract_first()
        print("N resultados: __{}__".format(n_resultados))
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


        for i,resultado in enumerate(resultado_en_resultados):

            ficha = resultado.xpath(x_path_resultado_in_tabla_resultados_ficha)
            print("RESULTADO: {}".format(i))
            print("..................................................................")
            

            ficha_txt = ficha.xpath(x_path_resultado_in_tabla_resultados_ficha_misc).extract()            
            print("FICHA: __{}__".format(ficha_txt))
            print("..................................................................")

            for linea_cleaned in [ ln.strip() for ln in ficha_txt if len(ln.strip()) > 0 ]:
                
                print("LINEA: {}".format(linea_cleaned))

                if "RELATOR" in linea_cleaned.upper():
                    print("Soy relator!")
                    print(linea_cleaned.split(':')[1].strip())    
                elif "PUBLICAÇÃO" in linea_cleaned.upper():
                    print("Soy fecha de publicación!")
                    print(linea_cleaned.split(':')[1].strip())
                elif "JULGADOR" in linea_cleaned.upper():
                    print("Soy organo julgadr!")
                    print(linea_cleaned.split(':')[1].strip())
                elif "JULGAMENTO" in linea_cleaned.upper():
                    print("Soy fecha de julgamento!")
                    print(linea_cleaned.split(':')[1].strip())

            num_proceso = ficha.xpath(x_path_resultado_in_tabla_resultados_ficha_num_proceso).extract_first()
            print("NUM PROCESO: __{}__".format(num_proceso.strip()))
            print("..................................................................")

            link = ficha.xpath(x_path_resultado_in_tabla_resultados_ficha_link_detalle).extract_first()
            print("LINK A DETALLE: __{}__".format(link))
            print("..................................................................")

            decisao = ficha.xpath(x_path_resultado_in_tabla_resultados_ficha_decisao).extract_first()
            print("TIPO DE DECISAO: __{}__".format(decisao))
            print("..................................................................")
        
            resumen = resultado.xpath(x_path_resultado_in_tabla_resultados_resumen)
            #print("RESUMEN: __{}__".format(resumen))


        # jurisprudencias = response.xpath('//*/table[@class="resultTable jurisprudencia"]/tbody/tr')
        # for jurisprudencia in jurisprudencias:
            # print('\n________________________')
            # print(jurisprudencias)
            #tipos = response.xpath('string(//*[@id="divDiminuir"]/div[14]/table/tbody/tr[3]/td[2]/table/tbody/tr[3]/td[1]')
            # tipos = response.xpath('string(//*[@id="divDiminuir"]/div[14]/table/tbody/tr[3]/td[2]/table/tbody/tr[2]/td[1]/div[2])')
            # for tipo in tipos:
            #     href = response.xpath('//*[@id="divDiminuir"]/div[14]/table/tbody/tr[3]/td[2]/table/tbody/tr[2]/td[1]/div[2]/a/@href')
            #     decisao = response.xpath('string(//*[@id="divDiminuir"]/div[14]/table/tbody/tr[3]/td[2]/table/tbody/tr[8]/td[1]/div[2]/font[2])')
            #     relator = response.xpath('')
            #     processo = response.xpath('')
            #     data_publicacao = response.xpath('')
            #     orgao = response.xpath('')
            #     data_julgamento = response.xpath('')
            # resumo = response.xpath('string(//*[@id="muda1"])')
            # print(tipos)
            # print(resumo)
            # print('\n________________________')