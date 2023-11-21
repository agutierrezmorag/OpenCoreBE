from django.shortcuts import render, get_object_or_404
from .models import News


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


def news_detail(request, pk):
    news = get_object_or_404(News, id=pk)
    return render(request, 'details.html', {'news': news})
