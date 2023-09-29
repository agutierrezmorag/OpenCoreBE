from django.db import models


class News(models.Model):
    POSITIVO = 'POSITIVO'
    NEUTRO = 'NEUTRO'
    NEGATIVO = 'NEGATIVO'
    SENTIMENT_CHOICES = [
        (POSITIVO, 'Positivo'),
        (NEUTRO, 'Neutro'),
        (NEGATIVO, 'Negativo'),
    ]

    title = models.CharField(max_length=150, blank=False)
    date_published = models.DateTimeField()
    date_pulled = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    website = models.CharField(max_length=50)
    link = models.URLField()
    sentiment = models.CharField(max_length=15, default='Neutro', choices=SENTIMENT_CHOICES)

    def __str__(self):
        return f'{self.title}, de {self.website} ({self.link})'
