from django.shortcuts import render
from collections import defaultdict
import numpy as np
from django.core.cache import cache
from .models import News
import json
import os


def read_json(filename, path):
    file_path = os.path.join(path, filename)
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data


def home(request):
    
    cached_data = cache.get('home_data')
    if cached_data:
        return render(request, 'index.html', cached_data)
    
    latest_news = News.objects.order_by('-date_published').first()
    recent_news = News.objects.order_by('-date_published')[1:21]
    negative_news = News.objects.filter(sentiment='Negativo')[:4]
    positive_news = News.objects.filter(sentiment='Positivo')[:4]
    neutral_news = News.objects.filter(sentiment='Neutro')[:20]

    context = {
        'latest_news': latest_news,
        'recent_news': recent_news,
        'negative_news': negative_news,
        'positive_news': positive_news,
        'neutral_news': neutral_news,
    }
    
    cache.set('home_data', context, timeout=3600)

    return render(request, 'index.html', context)


def search(request):
    path_to_json = '../indexador/results'
    data = cache.get('search_data')
    
    if data is None:
        data = read_json('index_historical.json', path_to_json)

        total_articles = len(data[0]['importance_scores'])

        idf_values = {word_data['word']: np.log(1 + (total_articles / word_data['frequency_global'])) for word_data in data}

        for word_data in data:
            for score in word_data['importance_scores']:
                article_frequency = score['frequency']
                article_word_count = score['article_info']['word_count']

                tf = article_frequency / article_word_count
                idf = idf_values[word_data['word']]
                tf_idf = tf * idf
                score['tf_idf'] = tf_idf

        for word_data in data:
            word_data['importance_scores'] = sorted(word_data['importance_scores'], key=lambda x: x['tf_idf'], reverse=True)
        
        cache.set('search_data', data, timeout=3600)

    query = request.POST.get('query', '')
    query_words = set(query.lower().split())

    # Crear conjuntos de palabras en los datos de TF-IDF
    tfidf_words = {word_data['word'] for word_data in data}

    # Encontrar la intersección de conjuntos para obtener palabras relevantes
    relevant_words = query_words.intersection(tfidf_words)

    word_scores = defaultdict(list)
    for word_tfidf in data:
        if word_tfidf['word'] in relevant_words:
            word_scores[word_tfidf['word']].extend(score['article_info']['article_id'] for score in word_tfidf['importance_scores'])

    article_ids = set(article_id for article_ids in word_scores.values() for article_id in article_ids)
    search_results = News.objects.filter(id__in=article_ids).distinct()

    total_results = len(search_results)

    return render(request, 'results.html', {'search_results': search_results, 'total_results': total_results})
