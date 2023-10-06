from urllib.parse import urljoin
import re
import datetime
import requests
from bs4 import BeautifulSoup
from scraper_noticias.utils import link_compare, clean_html
from scraper_noticias.selectors import tags, links, title_selector, content_selector


def news_collector(html, depth, website):
    # this will receive the response.text from the fetch_webpage function
    # the depth parameter will be used to determine how many news pages we want to scrape from that html
    # the idea is to have a list of news objects, each object will have a title, content and secondary headings
    news_list = []
    if html:
        news_container = (extract_tags(html, tags[website]['container'], tags[website]['value'], tags[website]['attribute'])
                 if isinstance(tags.get(website), dict)
                 else extract_tags(html, tags[website][0]))
        news_container = news_container[:depth]
        for container in news_container:
            # in the current container we either look for href in the current tag or in the first a tag
            a_tag = container.find('a') if container.name != 'a' else container

            if a_tag:
                link = a_tag.get('href')
                if not link_compare(links[website][0], link):
                    link = urljoin(links[website][0], link)
                news_html = fetch_webpage(link)
                if news_html:
                    news_html = clean_html(news_html)
                    #opened_container will be body tag 
                    opened_container = extract_tags(news_html, 'body')[0]
                    news_title = extract_news_title(opened_container, website)
                    news_content = extract_news_content(opened_container, website)
                    news_list.append({
                        # website will be the domain of the website
                        'website': website.split('.')[0],
                        'title': news_title,
                        'content': news_content,
                        'date': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        'link': link,
                    })
    return news_list


def fetch_webpage(url):
    '''
    Esta función recibe un link y retorna el html de la página web sin formato
    '''
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            return response.text
        else:
            print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
            return None
    except Exception as e:
        print(f"An error occurred while fetching the webpage: {str(e)}")
        return None


def extract_tags(html, tag, attrs_custom=None, attr_type=None):
    '''
    Esta función recibe el html de una página web, la tag que se quiere extraer y los atributos de la tag
    Retorna una lista con todas las tags que coincidan con los atributos
    '''
    if html:
        soup = BeautifulSoup(html, 'html.parser')
        return soup.select(f'{tag}[{attr_type}^="{attrs_custom}"]') if attrs_custom and attr_type else soup.select(tag)
    return None


def extract_tags_from_container(container, sub_container, attrs_custom=None, attr_type=None):
    '''
    Esta función recibe un contenedor(etiqueta html), un sub contenedor, la tag que se quiere extraer y los atributos de la tag
    Retorna una lista con todas las tags que coincidan con los atributos
    TODO: está función fue desarrollada con latecera en mente, posible candidato a refactorizar
    '''
    if container:
        if attrs_custom and attr_type:
            return container.find_all(sub_container, attrs={attr_type: attrs_custom})
        else:
            return container.find_all(sub_container)
    return None


def extract_news_title(container, website):
    '''
    Esta función recibe el contenedor(etiqueta html) donde se encuentra el titulo de la noticia y el sitio web
    Retorna el titulo de la noticia
    website se utiliza para saber que selector utilizar correspondiente al sitio web
    TODO: Posible candidato a refactorizar
    '''
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
    '''
    Esta función recibe el contenedor(etiqueta html) donde se encuentra el contenido de la noticia y el sitio web
    Retorna el contenido de la noticia
    website se utiliza para saber que selector utilizar correspondiente al sitio web
    '''
    regex = re.compile(r'[\n\t\\]| {2,}')
    #extrae el contenido utilizando los selectores de contenido
    content = ""
    #chequea si el selector tiene un contenedor, valor y atributo
    if isinstance(content_selector[website], dict):
        container = extract_tags_from_container(container, content_selector[website]['container'], content_selector[website]['value'], content_selector[website]['attribute'])
    else:
        container = extract_tags_from_container(container, content_selector[website][0])
    if container:
        for tag in container:
            content += regex.sub('', tag.text.strip())
    else:
        return None
    return content
