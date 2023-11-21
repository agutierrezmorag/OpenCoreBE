from django.shortcuts import render, get_object_or_404
from django.db.models import Q
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


def search(request):
    query = request.POST.get('query', None)
    search_results = News.objects.filter(Q(content__icontains=query) | Q(title__icontains=query))
    print(search_results)
    return render(request, 'results.html', {'search_results': search_results})
