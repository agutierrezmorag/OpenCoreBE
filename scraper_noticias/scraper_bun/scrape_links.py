import sys
import os
sys.path.append(os.path.dirname(os.getcwd()) + "/OpenCoreBE") 
from scraper_noticias.web_scraper import fetch_webpage, extract_links,clean_html
from scraper_noticias.data_processing import save_to_json
from scraper_noticias.selectors import links,tags

if __name__ == "__main__":
    news_links = []
    for website, link_list in links.items():
        for link in link_list:
            html = fetch_webpage(link)
            if html:
                html = clean_html(html)
                news_links.extend(extract_links(html, website))
            else:
                print(f'Error al obtener el html de {website}')
    save_to_json(news_links, 'news_links.json', os.path.join(os.path.dirname(__file__), 'bun_jsons/'), overwrite=True)