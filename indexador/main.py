import os
from indexer import indexer
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from scraper_noticias.data_processing import save_to_json, read_json

if __name__ == "__main__":
    palabras = []
    #historical json will look for the index_historical.json file in the results folder
    historical_json = None
    if os.path.exists(os.path.join(os.path.dirname(__file__), 'results', 'index_historical.json')):
        historical_json = read_json('index_historical.json', os.path.join(os.path.dirname(__file__), 'results'))
    indexador = indexer(historical_json)
    palabras.extend(indexador)
    save_to_json(palabras, 'index.json', os.path.join(os.path.dirname(__file__), 'results'), overwrite=True)
    save_to_json(palabras, 'index_historical.json', os.path.join(os.path.dirname(__file__), 'results'))