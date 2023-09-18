from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup

def link_compare(website_link, new_link):
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

def clean_html(html):
    if html:
        soup = BeautifulSoup(html, 'html.parser')
        for script in soup(['script', 'style']):
            script.extract()
        return soup.prettify()
    return None