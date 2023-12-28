from datetime import timedelta, datetime

from decouple import config
from django.core.cache import cache
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import render
from django.views.decorators.cache import cache_page
from pymongo import MongoClient
from pymongo.server_api import ServerApi


def get_db_client():
    """
    Retrieves the 'news_news' collection from the 'opencoredatabase' database.

    Returns:
        pymongo.collection.Collection: The 'news_news' collection.
    """
    client = MongoClient(config("MONGO_URI"), server_api=ServerApi("1"))
    return client


def get_news(sentiment=None, limit=None):
    """
    Retrieve news articles from the database based on the specified sentiment and limit.

    Args:
        sentiment (str, optional): The sentiment of the news articles to retrieve. Defaults to None.
        limit (int, optional): The maximum number of news articles to retrieve. Defaults to None.

    Returns:
        list: A list of news articles matching the specified sentiment and limit.
    """
    client = get_db_client()
    db = client["opencoredatabase"]
    collection = db["news_news"]
    two_weeks_ago = datetime.now() - timedelta(weeks=2)

    query = {"date_published": {"$gte": two_weeks_ago}}
    if sentiment:
        query["sentiment"] = sentiment

    news = collection.find(query).sort("date_published", -1)

    if limit:
        news = news.limit(limit)

    cache_key = f"news_{sentiment}_{limit}"
    cached_news = cache.get(cache_key)
    if cached_news is not None:
        return cached_news

    news = list(news)
    cache.set(cache_key, news, 3600)

    return news


@cache_page(60 * 60)
def home(request):
    """
    Renders the home page with news data.

    Parameters:
    - request: The HTTP request object.

    Returns:
    - A rendered HTML template with news data.
    """
    client = get_db_client()
    db = client["opencoredatabase"]
    collection = db["news_news"]
    latest_news = get_news(limit=5)
    recent_news = get_news(limit=24)[5:]
    negative_news = get_news(sentiment="Negativo", limit=20)
    positive_news = get_news(sentiment="Positivo", limit=20)

    total_news = collection.count_documents({})
    total_words = sum(len(news["content"].split()) for news in collection.find({}))

    context = {
        "latest_news": latest_news,
        "recent_news": recent_news,
        "negative_news": negative_news,
        "positive_news": positive_news,
        "total_news": total_news,
        "total_words": total_words,
    }

    return render(request, "index.html", context)


def sort_results(request, search_results):
    """
    Sorts the search results based on the specified sort option.

    Args:
        request (HttpRequest): The HTTP request object.
        search_results (list): The list of search results.

    Returns:
        list: The sorted search results.
    """
    sort_option = request.GET.get("sort", "relevance")

    if sort_option in ["newest", "oldest"]:
        reverse = sort_option == "newest"
        search_results.sort(key=lambda doc: doc["date_published"], reverse=reverse)

    return search_results


def search(request):
    """
    Perform a search based on the provided query, sentiments, and sources.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The rendered search results page.

    Raises:
        None
    """
    client = get_db_client()
    db = client["opencoredatabase"]
    collection = db["news_news"]
    try:
        now = datetime.now()
        two_weeks_ago = now - timedelta(days=14)

        search_query = request.GET.get("query")
        sentiments = request.GET.getlist("sentiment")
        sources = request.GET.getlist("source")

        cache_key = (
            "search_results_"
            + "".join(e for e in search_query if e.isalnum())
            + "_sentiments_"
            + "_".join(sentiments)
            + "_sources_"
            + "_".join(sources)
        )
        results = cache.get(cache_key)
        if results is None:
            pipeline = [
                {
                    "$search": {
                        "index": "news_index",
                        "text": {"query": search_query, "path": {"wildcard": "*"}},
                    }
                },
                {
                    "$match": {
                        "date_published": {"$gte": two_weeks_ago},
                    }
                },
            ]
            if sentiments:
                pipeline.append(
                    {
                        "$match": {
                            "sentiment": {"$in": sentiments},
                        }
                    }
                )
            if sources:
                pipeline.append(
                    {
                        "$match": {
                            "website": {"$in": sources},
                        }
                    }
                )
            results = collection.aggregate(pipeline)
            results = list(results)
            cache.set(cache_key, results, 60 * 15)

        results = sort_results(request, results)
        total_results = len(results)

        page_number = request.GET.get("page", 1)
        paginator = Paginator(results, 25)

        try:
            page_obj = paginator.page(page_number)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)

        context = {
            "page_obj": page_obj,
            "total_results": total_results,
            "query": search_query,
            "sources": request.GET.getlist("source"),
            "sentiment": request.GET.getlist("sentiment"),
            "sort": request.GET.get("sort", "relevance"),
        }

        return render(request, "results.html", context)
    finally:
        client.close()


def stats(request):
    return render(request, "stats.html")
