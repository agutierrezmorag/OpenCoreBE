import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from urllib.parse import urlparse

# Define your scraping parameters
links = {
    '24horas': ['https://www.24horas.cl/actualidad/politica'],
}

# Function to scrape news titles
def scrape_titles_links_content_and_images(site, url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Extract titles, links, content, and images based on a more flexible approach
    article_containers = soup.find_all('article', class_='col')

    if article_containers:
        data = []
        for article_container in article_containers:
            title_container = article_container.find('h3', class_='tit')
            title = title_container.text.strip()

            link_element = article_container.find('a', href=True)
            if link_element:
                link = urljoin(url, link_element['href'])

                # Access the link of the full article
                full_article_response = requests.get(link)
                full_article_soup = BeautifulSoup(full_article_response.text, 'html.parser')

                # Extract content from <p> tags within the specified container
                content_container = full_article_soup.find('section', class_='art-content')
                if content_container:
                    content_body = content_container.find('div', class_='CUERPO')
                    paragraphs = content_body.find_all('p') if content_body else []

                    content = ' '.join([p.text.strip() for p in paragraphs])
                else:
                    content = "Content not found."

                # Extract image URL from <figure> tag
                image_container = article_container.find('figure', class_='img-wrap')
                image_url = image_container.find('img')['data-src'] if image_container else None

                # Extract website from the base URL
                parsed_url = urlparse(url)
                website = parsed_url.netloc.split('.')[1]  # Change here

                # Extract date of publication if available
                date_container = article_container.find('p', class_='fecha')
                date = date_container.text.strip() if date_container else "Date not found"

                data.append({'title': title, 'link': link, 'content': content, 'image_url': image_url, 'website': website, 'date': date})
            else:
                # Handle the case where the link is not found
                print(f"Warning: No link found for the title '{title}'.")

        return data
    else:
        return None

# Example usage for the given link
site = '24horas'
url = links[site][0]
data = scrape_titles_links_content_and_images(site, url)

if data:
    for i, entry in enumerate(data, 1):
        print(f"{i}. Website: {entry['website']}")
        print(f"   Title: {entry['title']}")
        print(f"   Link: {entry['link']}")
        print(f"   Content: {entry['content']}")
        print(f"   Image URL: {entry['image_url']}")
        print(f"   Date: {entry['date']}")
        print()
else:
    print("No titles found.")