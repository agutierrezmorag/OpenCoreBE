from django.db import models
from django.utils import timezone


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
    date_published = models.DateTimeField(default=timezone.now)
    date_pulled = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    img_url = models.URLField(blank=True, null=True)
    website = models.CharField(max_length=50)
    link = models.URLField()
    sentiment = models.CharField(max_length=15, default='Neutro', choices=SENTIMENT_CHOICES)

    class Meta:
        indexes = [
            models.Index(fields=['date_published']),
        ]

    def __str__(self):
        return f'{self.title} ({self.website})'
