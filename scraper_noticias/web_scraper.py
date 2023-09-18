from urllib.parse import urljoin
import re
import datetime
import requests
from bs4 import BeautifulSoup
from scraper_noticias.utils import link_compare, clean_html
from scraper_noticias.selectors import tags, links, title_selector, content_selector


def news_collector(html, depth, website):
    #this will receive the response.text from the fetch_webpage function
    #the depth parameter will be used to determine how many news pages we want to scrape from that html
    #the idea is to have a list of news objects, each object will have a title, content and secondary headings
    news_list = []
    if html:
        news_container = extract_tags(html, tags[website][0])
        news_container = news_container[:depth]
        for container in news_container:
            #we look for a link to the new page then we fetch the html from that page
            a_tag = container.find('a')
            if a_tag:
                link = a_tag.get('href')
                if not link_compare(links[website][0], link):
                    link = urljoin(links[website][0], link)
                news_html = fetch_webpage(link)
                if news_html:
                    news_html = clean_html(news_html)
                    opened_container = extract_tags(news_html, tags[website][0])
                    opened_container = opened_container[0]
                    news_title = extract_news_title(opened_container, website)
                    news_content, news_secondary_headings = extract_news_content(opened_container, website)
                    news_list.append({
                        #website will be the domain of the website
                        'website': website.split('.')[0],
                        'title': news_title,
                        'content': news_content,
                        'secondary_headings': news_secondary_headings,
                        'date': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        'link': link,
                    })
    return news_list

def fetch_webpage(url):
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

def extract_tags(html, tag, attrs=None):
    if html:
        soup = BeautifulSoup(html, 'html.parser')
        return soup.find_all(tag, attrs)
    return None

def extract_tags_from_container(container, sub_container, attrs=None, attr_type=None):
    if container:
        if attrs and attr_type:
            return container.find_all(sub_container)
        else:
            return container.find_all(sub_container)
    return None

def extract_news_title(container, website):
    selector = title_selector[website]
    container = extract_tags_from_container(container, selector['container'], selector['value'], selector['attribute'])
    if container:
        return container[0].text.strip()
    else:
        #extract h1 tag
        container = extract_tags_from_container(container, 'h1')
        if container:
            #remove \n and \t from the title
            regex = re.compile(r'[\n\t]')
            return regex.sub('', container[0].text.strip())
    return None

def extract_news_content(container, website):
    #exract the news content using the dictionary of selectors
    content = ""
    secondary_headings = []
    for selector in content_selector[website]:
        for tag in container.find_all(content_selector[website][selector]):
            if selector == 'news_content':
                content += tag.text.strip()
            elif selector == 'news_secondary_headings':
                #search for a container with text content inside of it and then append it to the list
                for child in tag.children:
                    if child.text.strip():
                        secondary_headings.append(child.text.strip())
    return content, secondary_headings