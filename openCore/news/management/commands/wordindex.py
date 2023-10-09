from django.core.management.base import BaseCommand
from news.models import News, WordIndex
import spacy
from collections import defaultdict
from sklearn.feature_extraction.text import TfidfVectorizer
from django.utils import timezone  # Import Django's timezone module
import time
from django.db import transaction
import bson

class Command(BaseCommand):
    help = 'Index words from new News articles using spaCy and TF-IDF'

    def handle(self, *args, **kwargs):
        print('current time: ', timezone.now())
        #carga el modelo de lenguaje español
        nlp = spacy.load("es_core_news_sm")

        #obtiene el id del último artículo indexado
        last_indexed_article_id = self.get_last_indexed_article_id()

        # obtiene los artículos de noticias nuevos publicados después del último artículo indexado
        new_news_articles = News.objects.filter(id__gt=last_indexed_article_id)
        print (new_news_articles.count())

        #cargado de stop words
        stop_words = spacy.lang.es.stop_words.STOP_WORDS

        for news_article in new_news_articles:
            #tokeniza, elimina las palabras vacías y pone en minúsculas las palabras en los documentos
            content = news_article.content
            doc = nlp(content)
            
            #lista de palabras filtradas(sin stop words)
            words = [token.text.lower() for token in doc if token.text.lower() not in stop_words and token.is_alpha]

            words_list = list(WordIndex.objects.values_list('word', flat=True)) #lista de palabras ya indexadas en la base de datos
            # indexado de palabras en el articulo
            for word in words:
                frequency = content.count(word)  # frecuencia de la palabra en el artículo
                imported_scored_id = bson.ObjectId() # id generado para mongodb
                with transaction.atomic():
                    if word not in words_list:
                        # if the word is not on the db, it will create a new record
                        word_index = WordIndex(word=word, importance_scores={'_id':imported_scored_id, 'article_id': news_article.id,'frequency': frequency})
                        word_index.save()
                        word_index.news.add(news_article)
                    else:
                        # if the word is on the db, it will update the record
                        word_index = WordIndex.objects.get(word=word)
                        word_index.importance_scores.append({'_id':imported_scored_id, 'article_id': news_article.id,'frequency': frequency})
                        word_index.news.add(news_article)
                        word_index.save()

                        


            # Update the record of the last indexed article to the most recent one in the batch
            self.update_last_indexed_article(news_article)
            self.stdout.write(self.style.SUCCESS(f'Indexed words for "{news_article.title}"'))
        print ('time after query: ', timezone.now())

    def get_last_indexed_article_id(self):
        # Implement a method to fetch the ID of the last indexed article from a configuration file or database
        # Return a default value (e.g., 0) if no previous indexing has been done
        try:
            last_indexed_article = News.objects.latest('indexed_on')
            return last_indexed_article.id
        except News.DoesNotExist:
            return 0

    def update_last_indexed_article(self, news_article):
        # Implement a method to update the 'indexed_on' field of the last indexed article
        # You can set 'indexed_on' to the current date and time using Django's timezone module
        news_article.indexed_on = timezone.now()
