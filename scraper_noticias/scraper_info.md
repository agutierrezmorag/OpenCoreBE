# Modulo: scraper

El script de scrapeo se encarga de extraer los datos necesarios para los diferentes modulos del sistema, estos son posteriormente almacenados en archivos json con el proposito de lograr una mejor manipulación de los datos.

## Librerias utilizadas
```
BeautifulSoup -> función: extraer datos de un archivo html o xml
requests -> función: cliente HTTP para extraer datos de una página web
urllib -> función: herramientas para trabajar con URLs
json -> función: codificar y decodificar archivos json
os -> función: interactuar con el sistema operativo(crear carpetas, archivos, etc)
re -> función: expresiones regulares
datetime -> función: trabajar con fechas y horas
```

## Explicación general
El modulo de scrapeo se dividio en 4 archivos agregado a un archivo main.py que se encarga de iniciar el ciclo de scrapeo, estos archivos son:
```
main.py -> inicia el ciclo de scrapeo
web_scraper.py -> contiene las funciones de scrapeo
utils.py -> contiene funciones auxiliares
data_processing.py -> contiene las funciones de procesamiento y almacenamiento de datos
selectors.py -> ARCHIVO IMPORTANTE, contiene las etiquetas html a scrapear de cada sitio web almacenadas en diccionarios
```
## selectors.py
Este archivo contiene los selectores de cada sitio web, estos son almacenados en diccionarios para facilitar su uso.

Actualmente existen 4 diccionarios.

### links
En este diccionario se almacenan los links de cada sitio web apuntando a la sección de politica.
```py
links = {
    'latercera': ['https://www.latercera.com/canal/politica/'],
}
```
### tags
Este diccionario contiene la etiqueta html donde se encuentran contenidas las noticias dentro del html extraido de los links.
```py
tags = {
    'latercera': ['article'],
    't13': {
        'container': 'div',
        'attribute': 'class',
        'value': 'card-normal t13-ui-card-normal'
    },
}
```
La idea es encontrar aquella etiqueta que las noticias comparten en comun, en la tercera es la etiqueta article, en cambio en t13 es un poco mas complejo por lo que se debe buscar una etiqueta que contenga solo las noticias de politica, en este caso es la etiqueta div con el atributo class y el valor card-normal t13-ui-card-normal.
```html
 <div class="card-normal t13-ui-card-normal"></div>
```
### title_selector
Este diccionario contiene la etiqueta html donde se encuentra el titulo de la noticia.
```py
title_selector = {
    'latercera': {
        'container': 'div',
        'attribute': 'class',
        'value': 'hl',
    },
}
```
### content_selector
Este diccionario contiene la etiqueta html donde se encuentra el contenido de la noticia.
```py
content_selector = {
    'latercera': {
        'news_content': 'p',
    }
}
```
TODO: Este diccionario 
