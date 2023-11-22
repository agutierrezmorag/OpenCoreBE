from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import News
import json
import os
from math import log

def read_json(filename, path):
    file_path = os.path.join(path, filename)
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data

def home(request):
    recent_news = News.objects.order_by('-date_published')[:4]
    negative_news = News.objects.filter(sentiment='Negativo')[:4]
    positive_news = News.objects.filter(sentiment='Positivo')[:4]
    neutral_news = News.objects.filter(sentiment='Neutro')[:4]

    context = {
        'recent_news': recent_news,
        'negative_news': negative_news,
        'positive_news': positive_news,
        'neutral_news': neutral_news,
    }

    return render(request, 'index.html', context)


def search(request):
    
    path_to_json = '../indexador/results'
    
    data = read_json('index_historical.json',path_to_json)
    
    total_articles = len(data[0]['importance_scores'])
    
    for word_data in data:
        word = word_data['word']
        word_frequency_global = word_data['frequency_global']
        
        for score in word_data['importance_scores']:
            article_frequency = score['frequency']
            article_word_count = score['article_info']['word_count']
            
            tf = article_frequency / article_word_count
            
            idf = log(1 + (total_articles / word_frequency_global))
            
            tf_idf = tf * idf
            
            score['tf_idf'] = tf_idf

            word_data['importance_scores'] = sorted(word_data['importance_scores'], key=lambda x: x['tf_idf'], reverse=True)
    
    querys = request.POST.get('query', None)
    
    articles = []
    
    querys = querys.split(' ')
    
    for query in querys:
        for word_tfidf in data:
            imp_word = word_tfidf['word']
            if query == imp_word:
                imp_scores = sorted(word_tfidf['importance_scores'], key=lambda x: x['tf_idf'], reverse=True)
                for imp_score in imp_scores:
                    articles.append(imp_score['article_info']['article_id'])
            
    search_results = News.objects.filter(id__in=articles)
    
    return render(request, 'results.html', {'search_results': search_results})
