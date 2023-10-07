from urllib.parse import urljoin
import re
import datetime
import requests
from bs4 import BeautifulSoup
from scraper_noticias.utils import link_compare, clean_html
from scraper_noticias.selectors import tags, links, title_selector, content_selector

def fetch_webpage(url):
    """
    Obtiene el contenido de una página web a partir de la URL proporcionada.

    Args:
        url (str): La URL de la página web que se desea obtener.

    Returns:
        str o None: El contenido de texto de la página web si la solicitud se realiza con éxito, o    None si ocurre un error durante la solicitud.

    Raises:
        None

    Esta función envía una solicitud HTTP GET a la URL especificada y devuelve
    el contenido de texto de la página web si la solicitud se realiza con éxito.
    Si ocurre un error durante la solicitud, imprime un mensaje de error y devuelve None.

    """
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()  # Levanta una excepcion si no se pudo hacer la peticion
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Ocurrio un error en la petición web: {str(e)}")
        return None

def extract_tags(html, tag, attrs_custom=None, attr_type=None):
    """
    Extrae elementos HTML que coinciden con una etiqueta especificada y atributos opcionales de un documento HTML.

    Args:
        html (str): El documento HTML como una cadena de texto.
        tag (str): La etiqueta HTML que se desea buscar (por ejemplo, 'div', 'a', 'p').
        attrs_type (str, opcional): tipo de atributo personalizado para coincidir (por ejemplo, 'class' o 'id').
        attr_custom (str, opcional): El valor del atributo para coincidir (por ejemplo, 'text-white').
                                   Solo se utiliza si se proporciona 'attrs_custom'.

    Returns:
        lista de objetos Tag: Una lista de objetos Tag de BeautifulSoup que representan los elementos HTML coincidentes,
                            o una lista vacía si no se encuentran elementos.

    Raises:
        None

    Esta función analiza el documento HTML de entrada utilizando BeautifulSoup y busca elementos HTML
    que coincidan con la etiqueta especificada 'tag' y el atributo opcional 'attrs_custom'. Devuelve una lista de objetos Tag
    que representan los elementos coincidentes o una lista vacía si no se encuentran elementos.

    Ejemplo de uso:
    >>> contenido_html = "<div class='container'><p>Hola, mundo!</p></div>"
    >>> extraer_etiquetas(contenido_html, 'div', 'container', 'class')
    [<div class="container"><p>Hola, mundo!</p></div>]

    """
    if html:
        soup = BeautifulSoup(html, 'html.parser')
        selector = f'{tag}[{attr_type}^="{attrs_custom}"]' if attrs_custom and attr_type else tag
        return soup.select(selector)
    return None

def extract_tags_from_container(container, sub_container, attrs_custom=None, attr_type=None):
    """
    Extrae elementos HTML que coincidan con una etiqueta de subcontenedor especificada y atributos opcionales
    de un elemento contenedor HTML dado.

    Args:
        container (Tag): El elemento contenedor HTML para extraer elementos coincidentes.
        sub_container (str): La etiqueta HTML que se buscará dentro del 'container'.
        attrs_custom (str, opcional): Valor de atributo personalizado para coincidir (por ejemplo, 'text-white').
        attr_type (str, opcional): El tipo de atributo para coincidir (por ejemplo, 'class', 'id').
                                   Solo se utiliza si se proporciona 'attrs_custom'.

    Returns:
        ResultSet: Un ResultSet de BeautifulSoup que contiene objetos Tag que representan los elementos HTML que coinciden con los criterios encontrados dentro del 'container', o un ResultSet vacío  si no hay elementos que cumplan los criterios.

    Raises:
        None

    Esta función busca elementos HTML dentro del elemento 'container' dado
    que coincidan con la etiqueta 'sub_container' especificada y el atributo opcional 'attrs_custom'. Devuelve
    un ResultSet que contiene objetos Tag que representan los elementos coincidentes o un ResultSet vacío si no hay elementos que cumplan los criterios.

    Ejemplo de uso:
    >>> container_html = "<div><p class='text'>¡Hola, mundo!</p><p>Otro párrafo.</p></div>"
    >>> container = BeautifulSoup(container_html, 'html.parser')
    >>> extract_tags_from_container(container, 'p', 'text', 'class')
    [<p class="text">¡Hola, mundo!</p>]

    """

    if container:
        if attrs_custom and attr_type:
            return container.find_all(sub_container, attrs={attr_type: attrs_custom})
        else:
            return container.find_all(sub_container)
    return None

def extract_news_title(container, website):
    """
    Extrae el título de un artículo de noticias a partir del elemento de contenedor HTML proporcionado, basándose en el selector de título especificado para el sitio web correspondiente.

    Args:
        container (Tag o ResultSet): El elemento de contenedor HTML o ResultSet que contiene
                                     elementos HTML.
        website (str): El nombre del sitio web del cual se está extrayendo el título.

    Returns:
        str o None: El título del artículo de noticias extraído como una cadena de texto,
                     o None si no se puede encontrar el título.

    Raises:
        None

    Esta función está diseñada para extraer el título de un artículo de noticias del elemento de
    contenedor HTML proporcionado, basándose en el selector de título definido para el sitio web
    especificado. Utiliza una expresión regular para limpiar el texto del título extraído.

    Ejemplo de uso:
    >>> container_html = "<div><h1 class='headline'>Últimas Noticias</h1></div>"
    >>> container = BeautifulSoup(container_html, 'html.parser')
    >>> extract_news_title(container, 'Ejemplo de Noticias')
    'Últimas Noticias'
    """
    regex = re.compile(r'[\n\t]')
    selector = title_selector[website]
    if selector['container'] and selector['value'] and selector['attribute']:
        container = extract_tags_from_container(container, selector['container'], selector['value'], selector['attribute'])
    else:
        container = extract_tags_from_container(container, selector['container'])
    
    if container:
        return regex.sub('', container[0].text.strip())
    else:
        container = extract_tags_from_container(container, 'h1')
        if container:
            return regex.sub('', container[0].text.strip())
    return None

def extract_news_content(container, website):
    """
    Extrae el contenido de un artículo de noticias del elemento contenedor HTML proporcionado
    basado en el selector de contenido del sitio web especificado.

    Args:
        container (Tag o ResultSet): El elemento contenedor HTML o ResultSet que contiene
                                      elementos HTML.
        website (str): El nombre del sitio web del cual se está extrayendo el contenido.

    Returns:
        str o None: El contenido del artículo de noticias extraído como una cadena, o None
                     si no se puede encontrar el contenido.

    Raises:
        None

    Esta función está diseñada para extraer el contenido de un artículo de noticias del elemento
    contenedor HTML proporcionado, basado en el selector de contenido definido para el sitio web
    especificado. Utiliza una expresión regular para limpiar el texto del contenido extraído.

    Ejemplo de uso:
    >>> container_html = "<div><p>Contenido de noticias de última hora...</p><p>Más contenido...</p></div>"
    >>> container = BeautifulSoup(container_html, 'html.parser')
    >>> extract_news_content(container, 'Ejemplo de Noticias')
    'Contenido de noticias de última hora...Más contenido...'

    """
    regex = re.compile(r'[\n\t\\]| {2,}')
    content = ""
    selector = content_selector[website]
    if isinstance(selector, dict):
        container = extract_tags_from_container(container, selector['container'], selector['value'], selector['attribute'])
    else:
        container = extract_tags_from_container(container, selector[0])
    
    if container:
        for tag in container:
            content += regex.sub('', tag.text.strip())
    else:
        return None
    return content

def news_collector(html, depth, website):
    """
    Recopila artículos de noticias a partir del código fuente HTML proporcionado, basándose en la estructura y profundidad especificadas del sitio web.

    Args:
        html (str): El código fuente HTML de la página web que contiene los artículos de noticias.
        depth (int): El número máximo de artículos de noticias a recopilar.
        website (str): El nombre del sitio web para el cual se están recopilando los artículos de noticias.

    Returns:
        lista de diccionarios: Una lista de diccionarios, cada uno representando un artículo de noticias con las siguientes claves:
            - 'website' (str): El nombre del sitio web.
            - 'title' (str): El título del artículo de noticias.
            - 'content' (str): El contenido del artículo de noticias.
            - 'date' (str): La fecha y hora de la recopilación en el formato "%Y-%m-%d %H:%M:%S".
            - 'link' (str): El enlace URL al artículo de noticias.

    Raises:
        None

    Esta función recopila artículos de noticias a partir del código fuente HTML proporcionado, basándose en la estructura
    y profundidad especificadas del sitio web. Extrae el título, el contenido y otra información de
    cada artículo y los devuelve como una lista de diccionarios.

    Ejemplo de uso:
    >>> html_contenido = "<div><a href='articulo1.html'>Artículo 1</a><a href='articulo2.html'>Artículo 2</a></div>"
    >>> recolector_noticias(html_contenido, 2, 'NoticiasEjemplo')
    [{'website': 'NoticiasEjemplo',
      'title': 'Título del Artículo 1',
      'content': 'Contenido del Artículo 1...',
      'date': '2023-10-07 12:34:56',
      'link': 'https://www.ejemplodenoticias.com/articulo1.html'},
     {'website': 'NoticiasEjemplo',
      'title': 'Título del Artículo 2',
      'content': 'Contenido del Artículo 2...',
      'date': '2023-10-07 12:34:56',
      'link': 'https://www.ejemplodenoticias.com/articulo2.html'}]

    """

    news_list = []
    if not html:
        return news_list
    
    news_container = tags.get(website)
    if isinstance(news_container, dict):
        news_container = extract_tags(html, news_container['container'], news_container['value'], news_container['attribute'])
    else:
        news_container = extract_tags(html, news_container[0])
    
    news_container = news_container[:depth]
    
    for container in news_container:
        a_tag = container.find('a') if container.name != 'a' else container
        if a_tag:
            link = a_tag.get('href')
            if not link_compare(links[website][0], link):
                link = urljoin(links[website][0], link)
            
            news_html = fetch_webpage(link)
            if news_html:
                news_html = clean_html(news_html)
                opened_container = extract_tags(news_html, 'body')[0]
                news_title = extract_news_title(opened_container, website)
                news_content = extract_news_content(opened_container, website)
                
                news_list.append({
                    'website': website.split('.')[0],
                    'title': news_title,
                    'content': news_content,
                    'date': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    'link': link,
                })
    return news_list