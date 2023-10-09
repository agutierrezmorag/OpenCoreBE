from django.core.management.base import BaseCommand
from news.models import News,WordIndex

class Command(BaseCommand):
    help = 'Remove words from the index'

    def handle(self, *args, **kwargs):
        # Remove all words from the index
        WordIndex.objects.all().delete()
        #set all news indexed_on to null
        News.objects.filter(indexed_on=None).update(indexed_on=None)
        print('All words have been removed from the index')