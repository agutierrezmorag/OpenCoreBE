from urllib.parse import urlparse, urljoin
from scraper_noticias.selectors import links_inside,links
from bs4 import BeautifulSoup

def link_compare(website_link, new_link):
    '''
    Esta función recibe dos links y retorna True si ambos links pertenecen al mismo dominio
    '''
    
    # Parse the website link and new link
    website_parts = urlparse(website_link)
    new_link_parts = urlparse(new_link)

    # Compare the netloc (domain) of both links
    if website_parts.netloc != new_link_parts.netloc:
        return False

    # Check if the new_link is a relative URL
    if not new_link_parts.path.startswith('/'):
        return False

    # Join the relative path of new_link with the netloc of the website_link
    full_new_link = urljoin(website_link, new_link)

    # Compare the full URLs
    return website_link == full_new_link

def check_in_links_inside(website, incoming_link):
    '''
    Esta función recibe el nombre de un sitio web y un link y retorna True si el link pertenece a la lista de links_inside
    '''
    if not incoming_link.startswith('/'):
        #check netloc of both links, if they are equal then proceed, if not return False
        website_parts = urlparse(links[website][0])
        incoming_link_parts = urlparse(incoming_link)
        if website_parts.netloc != incoming_link_parts.netloc:
            return False
        else:
            incoming_link = incoming_link_parts.path

    website_parts = urlparse(links[website][0])
    incoming_link_parts = urlparse(incoming_link)
    links_inside_website = links_inside[website]

    #print type of website_parts.netloc
    print(type(website_parts.netloc))
    print(type(links[website][0]))
    modified_website_netloc = "https://"+ website_parts.netloc + "/"
    full_link = urljoin(modified_website_netloc, incoming_link_parts.path)
    full_link = full_link.split('/')
    for link in links_inside_website:
        link = link.split('/')
        #from the link inside array remove the empty strings ('')
        link = [x for x in link if x != '']
        full_link = [x for x in full_link if x != '']
        link_len = len(link)
        if full_link[:link_len] != link:
            continue
        return True
    return False


def clean_html(html):
    '''
    Está función recibe el html de una página web y retorna el html sin las etiquetas <script> y <style>
    ademas de darle un formato legible al html
    '''
    if html:
        soup = BeautifulSoup(html, 'html.parser')
        for script in soup(['script', 'style']):
            script.extract()
        return soup.prettify()
    return None