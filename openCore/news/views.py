import json
import os
from collections import defaultdict
from datetime import timedelta

import numpy as np
from django.core.cache import cache
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import render
from django.utils import timezone

from .models import News


def read_json(filename, path):
    """
    Read and parse a JSON file.

    Args:
        filename (str): The name of the JSON file.
        path (str): The path to the directory containing the JSON file.

    Returns:
        dict: The parsed JSON data.

    Raises:
        FileNotFoundError: If the specified file does not exist.
        JSONDecodeError: If the file is not a valid JSON file.
    """
    file_path = os.path.join(path, filename)
    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)
    return data


def get_news(sentiment=None, limit=None):
    """
    Retrieve news articles based on optional sentiment and limit parameters.

    Args:
        sentiment (str, optional): The sentiment of the news articles. Defaults to None.
        limit (int, optional): The maximum number of news articles to retrieve. Defaults to None.

    Returns:
        list: A list of news articles matching the specified criteria.
    """
    two_weeks_ago = timezone.now() - timedelta(weeks=2)
    news = News.objects.filter(date_published__gte=two_weeks_ago).order_by(
        "-date_published"
    )

    if sentiment:
        news = news.filter(sentiment=sentiment)
    if limit:
        news = news[:limit]

    cache_key = f"news_{sentiment}_{limit}"
    cached_news = cache.get(cache_key)
    if cached_news is not None:
        return cached_news

    news = list(news)
    cache.set(cache_key, news, 3600)

    return news


def home(request):
    """
    Renders the home page with news data.

    Parameters:
    - request: The HTTP request object.

    Returns:
    - A rendered HTML template with news data.
    """
    cached_data = cache.get("home_data")
    if cached_data:
        return render(request, "index.html", cached_data)

    latest_news = get_news(limit=5)
    recent_news = get_news(limit=24)[5:]
    negative_news = get_news(sentiment="Negativo", limit=20)
    positive_news = get_news(sentiment="Positivo", limit=20)

    context = {
        "latest_news": latest_news,
        "recent_news": recent_news,
        "negative_news": negative_news,
        "positive_news": positive_news,
    }

    cache.set("home_data", context, timeout=3600)

    return render(request, "index.html", context)


def filter_results(request, search_results):
    """
    Apply filters to the search results based on the user's selections.

    Args:
        request (HttpRequest): The HTTP request object.
        search_results (QuerySet): The search results to filter.

    Returns:
        QuerySet: The filtered search results.
    """
    sources = request.GET.getlist("source")
    if sources:
        search_results = search_results.filter(website__in=sources)
    sentiment = request.GET.getlist("sentiment")
    if sentiment:
        search_results = search_results.filter(sentiment__in=sentiment)
    sort_option = request.GET.get("sort", "relevance")
    if sort_option == "newest":
        search_results = search_results.order_by("-date_published")
    elif sort_option == "oldest":
        search_results = search_results.order_by("date_published")

    return search_results


def search(request):
    """
    Perform a search based on the user's query and return the search results.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The HTTP response containing the search results.
    """
    path_to_json = "../indexador/results"
    data = cache.get("search_data")

    if data is None:
        data = read_json("index_historical.json", path_to_json)

        total_articles = len(data[0]["importance_scores"])

        idf_values = {
            word_data["word"]: np.log(
                1 + (total_articles / word_data["frequency_global"])
            )
            for word_data in data
        }

        for word_data in data:
            for score in word_data["importance_scores"]:
                article_frequency = score["frequency"]
                article_word_count = score["article_info"]["word_count"]

                tf = article_frequency / article_word_count
                idf = idf_values[word_data["word"]]
                tf_idf = tf * idf
                score["tf_idf"] = tf_idf

            word_data["importance_scores"] = sorted(
                word_data["importance_scores"], key=lambda x: x["tf_idf"], reverse=True
            )

        cache.set("search_data", data, timeout=3600)

    query = request.GET.get("query", "")
    query_words = set(query.lower().split())
    query_cache_key = f"search_results_{query}"
    search_results = cache.get(query_cache_key)

    if search_results is None:
        tfidf_words = {word_data["word"] for word_data in data}

        relevant_words = query_words.intersection(tfidf_words)

        word_scores = defaultdict(list)
        for word_tfidf in data:
            if word_tfidf["word"] in relevant_words:
                importance_scores = word_tfidf["importance_scores"]
                word_scores[word_tfidf["word"]].extend(
                    score["article_info"]["article_id"] for score in importance_scores
                )

        article_ids = set(
            article_id for ids in word_scores.values() for article_id in ids
        )

        search_results = News.objects.filter(id__in=article_ids)

        cache.set(query_cache_key, search_results, timeout=3600)

    search_results = filter_results(request, search_results)

    total_results = search_results.count()
    page_number = request.GET.get("page", 1)
    paginator = Paginator(search_results, 25)

    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    context = {
        "page_obj": page_obj,
        "total_results": total_results,
        "query": query,
        "sources": request.GET.getlist("source"),
        "sentiment": request.GET.getlist("sentiment"),
        "sort": request.GET.get("sort", "relevance"),
    }

    return render(
        request,
        "results.html",
        context,
    )


def stats(request):
    return render(request, "stats.html")
