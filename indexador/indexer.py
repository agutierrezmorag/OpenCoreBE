import spacy
import time
from django.db import transaction
import bson
import django
from django.utils import timezone  # Import Django's timezone module
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '../openCore'))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "openCore.settings")
django.setup()
from news.models import News, WordIndex, ImportanceScore

def indexer():
    print('current time: ', timezone.now())
    #carga el modelo de lenguaje español
    nlp = spacy.load("es_core_news_sm")

    #obtiene el id del último artículo indexado
    last_indexed_article_id = get_last_indexed_article_id()

    # obtiene los artículos de noticias nuevos publicados después del último artículo indexado
    new_news_articles = News.objects.filter(id__gt=last_indexed_article_id)
    print (new_news_articles.count())

    #cargado de stop words
    stop_words = spacy.lang.es.stop_words.STOP_WORDS

    word_list_to_save = []
    for news_article in new_news_articles:
        #tokeniza, elimina las palabras vacías y pone en minúsculas las palabras en los documentos
        content = news_article.content
        doc = nlp(content)
        
        #lista de palabras filtradas(sin stop words)
        words = [token.text.lower() for token in doc if token.text.lower() not in stop_words and token.is_alpha]
        words = list(set(words)) #elimina duplicados

        db_words_list = set(WordIndex.objects.values_list('word', flat=True)) #lista de palabras ya indexadas en la base de datos
        # indexado de palabras en el articulo
        for word in words:
            frequency = content.lower().count(word)
            #si la palabra no esta en la base de datos ni en la lista de palabras a guardar, se agrega a la lista de palabras a guardar
            if word not in db_words_list and word not in [word["word"] for word in word_list_to_save]:
                word_list_to_save.append({
                    "word": word,
                    "frequency_global": frequency,
                    "importance_scores": [
                        {
                            "id_noticia": news_article.id,
                            "frequency": frequency
                        }
                    ],
                    "tf_idf_score": 0.0
                })
            elif word in [word["word"] for word in word_list_to_save]:
                #if word is already in the list, append a dict to the importance_scores list with the id_noticia and frequency
                for word_dict in word_list_to_save:
                    if word_dict["word"] == word:
                        word_dict["frequency_global"] += frequency
                        word_dict["importance_scores"].append({
                            "id_noticia": news_article.id,
                            "frequency": frequency
                        })
        # Update the record of the last indexed article to the most recent one in the batch
        update_last_indexed_article(news_article)
        print("indexed article: ", news_article.id)
    return word_list_to_save
    print ('time after query: ', timezone.now())

def get_last_indexed_article_id():
    # Implement a method to fetch the ID of the last indexed article from a configuration file or database
    # Return a default value (e.g., 0) if no previous indexing has been done
    try:
        last_indexed_article = News.objects.latest('indexed_on')
        if last_indexed_article.indexed_on is None:
            return 0
        return last_indexed_article.id
    except News.DoesNotExist:
        return 0

def update_last_indexed_article(news_article):
    # Implement a method to update the 'indexed_on' field of the last indexed article
    # You can set 'indexed_on' to the current date and time using Django's timezone module
    news_article.indexed_on = timezone.now()

