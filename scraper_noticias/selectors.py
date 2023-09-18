tags = {
    'latercera': ['article'],
    't13': ['article'],
}

links = {
    'latercera': ['https://www.latercera.com/canal/politica/'],
}

title_selector = {
    'latercera': {
        'container': 'div',
        'attribute': 'class',
        'value': ' hl',
    },
}

content_selector = {
    #in latercera, news content is inside a <p> tag and sometimes a h2 tag
    'latercera': {
        'news_content': 'p',
        'news_secondary_headings': 'h2',
    }
}