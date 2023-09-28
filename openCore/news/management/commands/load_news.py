import json
from django.core.management.base import BaseCommand
from openCore.news.models import News


class Command(BaseCommand):
    help = 'Importar datos de news_scraper a la base de datos'

    def handle(self, *args, **options):
        json_file = 'db/newsdb.json'

        try:
            with open(json_file, 'r') as file:
                data = json.load(file)
            for item in data:
                News.objects.create(**item)

            self.stdout.write(self.style.Success('Data loaded successfully into database'))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error loading data. Error {str(e)}'))
