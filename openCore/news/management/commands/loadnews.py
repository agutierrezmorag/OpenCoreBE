import json, os
from django.core.management.base import BaseCommand
from news.models import News


class Command(BaseCommand):
    help = 'Importar datos de news_scraper a la base de datos'

    def handle(self, *args, **options):
        json_file = 'newsdb.json'

        try:
            with open(json_file, 'r', encoding='utf-8') as file:
                data = json.load(file)
            for item in data:
                news_item = News(
                    title=item['title'],
                    date_published=item['date'],
                    content=item['content'],
                    website=item['website'],
                    link=item['link']
                )
                news_item.save()

            self.stdout.write(self.style.SUCCESS('Data loaded successfully into the database'))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error loading data. Error {str(e)}'))
