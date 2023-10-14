import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

links = {
    'cooperativa': ['https://www.cooperativa.cl/noticias/site/tax/port/fid_noticia/cooperativataxport_3_156_1483_1.html']
}

def scrape_titles_and_links(base_url, url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    anchor_tags = soup.find_all('a')
    titles_and_links = []

    for anchor_tag in anchor_tags:
        title_tag = anchor_tag.find('h3', class_='titular')

        if title_tag:
            title = title_tag.text.strip()
            relative_link = anchor_tag.get('href')
            absolute_link = urljoin(base_url, relative_link)
            titles_and_links.append((title, absolute_link))

    return titles_and_links

def scrape_full_notice(base_url, url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    paragraphs = soup.find_all('p')
    content = '\n'.join([p.text.strip() for p in paragraphs])

    # Extract the date of publication
    date_tag = soup.find('time', class_='hora') or soup.find('div', class_='fecha-publicacion')
    date_of_publication = date_tag.text.strip() if date_tag else "Date not found"

    return content, date_of_publication

def scrape_portrait_image(base_url, url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Look for the <picture> tag containing the <img> tag
    picture_tag = soup.find('picture')

    # Extract the image URL from the <img> tag within <picture>
    if picture_tag:
        img_tag = picture_tag.find('img')
        if img_tag:
            portrait_image_url = urljoin(base_url, img_tag.get('data-src'))
            return portrait_image_url

    # Return None if no portrait image found
    return None

base_url = 'https://www.cooperativa.cl'
cooperativa_links = links['cooperativa']
article_contents = []

for link in cooperativa_links:
    cooperativa_titles_and_links = scrape_titles_and_links(base_url, link)

    for i, (title, link) in enumerate(cooperativa_titles_and_links, start=1):
        full_link = urljoin(base_url, link)
        article_content, date_of_publication = scrape_full_notice(base_url, full_link)
        portrait_image_url = scrape_portrait_image(base_url, full_link)

        article_contents.append((title, full_link, article_content, date_of_publication, portrait_image_url))

        print(f"Article {i}: {title}\nLink: {full_link}\nContent:\n{article_content}\nDate of Publication: {date_of_publication}\nPortrait Image URL: {portrait_image_url}\n")
