import os
from indexer import indexer
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from scraper_noticias.data_processing import save_to_json

if __name__ == "__main__":
    palabras = []
    indexador = indexer()
    palabras.extend(indexador)
    save_to_json(palabras, 'index.json', os.path.join(os.path.dirname(__file__), 'results'), overwrite=True)
    save_to_json(palabras, 'index_historical.json', os.path.join(os.path.dirname(__file__), 'results'))