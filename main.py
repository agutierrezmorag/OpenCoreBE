from scraper_noticias.web_scraper import fetch_webpage, news_collector
from scraper_noticias.data_processing import save_to_json
from scraper_noticias.utils import clean_html
from scraper_noticias.selectors import links
import os


if __name__ == "__main__":
    noticias = []
    for website, link_list in links.items():
        for link in link_list:
            html = fetch_webpage(link)
            if html:
                html = clean_html(html)
                news_list = news_collector(html, 5, website)
                if news_list:
                    noticias.extend(news_list)
    save_to_json(noticias, 'newsdb.json', os.path.join(os.path.dirname(__file__), 'openCore'), overwrite=True)
    save_to_json(noticias, 'newsdb_historical.json', os.path.join(os.path.dirname(__file__), 'openCore'))