from django.db import models


class News(models.Model):
    title = models.CharField(max_length=150, blank=False)
    date_published = models.DateTimeField()
    date_pulled = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    website = models.CharField(max_length=50)
    link = models.URLField()
    sentiment = models.CharField(max_length=15, default='Neutro')

    def __str__(self):
        return f'{self.title}, de {self.website} ({self.link})'
