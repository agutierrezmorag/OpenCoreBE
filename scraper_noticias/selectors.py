# Este archivo contiene las etiquetas html que se van a extraer de las paginas de noticias

#La idea es modificar el scraper de tal forma que sea capaz de extraer noticias de otros sitios web de forma general
#Con ese scraper solo bastaria con agregar las etiquetas html en este archivo y el scraper se encargaria de extraer las noticias
#Los funciones a modificar se encuentran en el archivo scraper_noticias/web_scraper.py

#tags: diccionario que guarda el contenedor donde se encuentran las noticias en la pagina principal de cada sitio web
tags = {
    'latercera': ['article'],
    't13': {
        'container': 'div',
        'attribute': 'class',
        'value': 'card-normal t13-ui-card-normal'
    },
    '24horas': ['section']
}

#links: diccionario que guarda el link de la pagina principal de cada sitio web
links = {
    'latercera': ['https://www.latercera.com/canal/politica/'],
    't13': ['https://www.t13.cl/politica/'],
    '24horas': ["https://www.24horas.cl/actualidad/politica"]
}


#title_selector: diccionario que guarda el selector de la etiqueta html donde se encuentra el titulo de la noticia
title_selector = {
    'latercera': {
        #en la tercera se encuentra dentro de un div con la clase 'h1' -> <div class="h1">
        'container': 'div',
        'attribute': 'class',
        'value': 'hl',
    },
    't13': {
        'container': 'a',
        'attribute': 'class',
        'value': 'ui-card__title',
    },
    '24horas': {
        'container': 'div',
        'attribute': 'class',
        'value': 'titular'
    }
}

#content_selector: diccionario que guarda el selector de la etiqueta html donde se encuentra el contenido de la noticia
content_selector = {
    'latercera': {
        #en la tercera se encuentra dentro de las etiquetas <p>
        'news_content': 'p',
        'news_secondary_headings': 'h2',
    },
    't13': {
        'news_content': 'div.card-normal__info',
        'news_secondary_headings': 'h2',
    },
    '24horas': {
        'news_content': 'p',
        'news_secondary_headings': 'h2'
    }
}
