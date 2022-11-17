import requests
from bs4 import BeautifulSoup
import time
import pandas as pd

venta_casas=[]
#LA URL DE LA PRIMER PAGINA QUEDA FUERA DEL FOR PORQUE ES LA QUE INICIA, 
#LUEGO SE VA INCREMENTANDO DENTRO DEL FOR PARA RECORRER LA SIGUIENTE PAGINA
#Y ASI HASTA LA ULTIMA
url = 'https://inmuebles.mercadolibre.com.ar/bsas-gba-oeste/venta-casas_Desde_49_NoIndex_True'

#SE REALIZA EL RECORRIDO DE TODAS LAS PAGINAS DE ESTA BUSQUEDA, EN ESTE CASO : 42
for x in range(1,42):

    r= requests.get(url)#EXTRAE LA INFORMACION PAGINA POR PAGINA
    
    soup = BeautifulSoup(r.content, 'html.parser') 

    content = soup.find_all('div', class_='ui-search-result__wrapper shops__result-wrapper')


    for propiedad in content:
        tipo = propiedad.find('span', class_="ui-search-item__group__element ui-search-item__subtitle shops__items-group-details").text
        precio= propiedad.find('span', class_="price-tag-amount").text
        dimension= propiedad.find('ul', class_="ui-search-card-attributes ui-search-item__group__element shops__items-group-details").text
        direccion= propiedad.find('span', class_="ui-search-item__group__element ui-search-item__location shops__items-group-details").text
        descripcion= propiedad.find('h2', class_="ui-search-item__title ui-search-item__group__element shops__items-group-details shops__item-title").text
        url= propiedad.find('a', class_="ui-search-result__content ui-search-link").get('href')

        propiedad_info = {
            'tipo': tipo,
            'precio': precio,
            'dimension': dimension,
            'direccion': direccion,
            'descripcion': descripcion,
            'url': url
        }
        venta_casas.append(propiedad_info)# CARGA LA LISTA CON LA INFORMACION  DE CADA PROPIEDAD

    #ACA SE GENERA LA CUENTA(AL DESCUBRIR EL INCREMENTO DENTRO DE LA URL)
    #PARA ASI PROSEGUIR EN EL PROXIMO CICLO CON LA EXTRACCION DE LOS DATOS DE ESA PAGINA
     
    cuenta=((49)*(x+1) )-x
    l=str(cuenta)
    url= 'https://inmuebles.mercadolibre.com.ar/bsas-gba-oeste/venta-casas_Desde_'+l+'_NoIndex_True'
    print(url)
print('casas en venta encontradas:', len(venta_casas))

#PASO LA LISTA A UN DATAFRAME
df = pd.DataFrame(venta_casas)
print(df.head())
df.to_csv('venta_casas.csv', index=False)#GENERO EL ARCHIVO CSV
