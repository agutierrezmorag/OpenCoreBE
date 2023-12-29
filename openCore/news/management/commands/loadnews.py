import json

from decouple import config
from django.core.management.base import BaseCommand
from django.utils import timezone
from pymongo import MongoClient
from pymongo.errors import BulkWriteError, PyMongoError
from pymongo.server_api import ServerApi


class Command(BaseCommand):
    help = "Importar datos de news_scraper a la base de datos"

    def handle(self, *args, **options):
        json_file = "newsdb.json"
        print("current time: ", timezone.now())

        client = MongoClient(config("MONGO_URI"), server_api=ServerApi("1"))
        db = client["opencoredatabase"]
        collection = db["news_news"]

        previous_news_uris = [news["link"] for news in collection.find({})]
        print("time after query: ", timezone.now())
        print(previous_news_uris)

        try:
            with open(json_file, "r", encoding="utf-8") as file:
                data = json.load(file)
            news_items = []
            for item in data:
                if item["link"] not in previous_news_uris:
                    date_published_str = item["date"]
                    date_published = timezone.make_aware(
                        timezone.datetime.strptime(
                            date_published_str, "%Y-%m-%d %H:%M:%S"
                        ),
                        timezone=timezone.get_current_timezone(),
                    )
                    news_item = {
                        "_id": item["link"],
                        "title": item["title"],
                        "date_published": date_published,
                        "content": item["content"],
                        "website": item["website"],
                        "link": item["link"],
                        "img_url": item["image_url"],
                        "sentiment": item["sentiment"],
                    }
                    news_items.append(news_item)
                    print("------------------------------")
                    print(f"Titulo: {item['title']} ")
                    print(f"Sentimiento: {item['sentiment']} ")
            if news_items:
                try:
                    collection.insert_many(news_items, ordered=False)
                except BulkWriteError as bwe:
                    print(bwe.details)

            self.stdout.write(
                self.style.SUCCESS("Data loaded successfully into the database")
            )

        except FileNotFoundError:
            self.stdout.write(self.style.ERROR("File not found."))

        except PyMongoError as e:
            self.stdout.write(self.style.ERROR(f"Error loading data. Error {str(e)}"))

        finally:
            client.close()
