import requests
from bs4 import BeautifulSoup

tags = {
    'latercera': ['article'],
}
links = {
    'latercera': ['https://www.latercera.com/canal/politica/'],
}

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

def clean_html(html):
    if html:
        soup = BeautifulSoup(html, 'html.parser')
        for script in soup(['script', 'style']):
            script.extract()
        return soup.prettify()
    return None

def extract_tags(html, tag):
    if html:
        soup = BeautifulSoup(html, 'html.parser')
        return soup.find_all(tag)
    return None

def save_html(html, filename):
    if html:
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(html)
        print(f"HTML saved to {filename}")

if __name__ == "__main__":
    for website, link_list in links.items():
        for link in link_list:
            html = fetch_webpage(link)
            if html:
                html = clean_html(html)
                save_html(html, f"{website}_{link.replace('/', '_').replace('.', '_')}.html")
                for tag in tags[website]:
                    tags_html = extract_tags(html, tag)
                    if tags_html:
                        save_html(str(tags_html), f"{website}_{link.replace('/', '_').replace('.', '_')}_{tag}.html")

        