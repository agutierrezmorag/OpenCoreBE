from djongo import models
from django import forms
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
    indexed_on = models.DateTimeField(null=True, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=['date_published']),
        ]

    def __str__(self):
        return f'{self.title} ({self.website})'


class ImportanceScore(models.Model):
    _id = models.ObjectIdField(primary_key=True)
    article_id = models.IntegerField()
    frequency = models.IntegerField(null=True, blank=True)


class ImportanceScoreForm(forms.ModelForm):
    class Meta:
        model = ImportanceScore
        fields = ['article_id', 'frequency']


class WordIndex(models.Model):
    word = models.CharField(max_length=50)  # Store the word itself
    news = models.ManyToManyField('News') # Reference to the News model
    frequency_global = models.PositiveIntegerField(null=True, blank=True)
    importance_scores = models.EmbeddedField(
        model_container=ImportanceScore,
        model_form_class=ImportanceScoreForm,
        null=True,
        blank=True
    )
    tf_idf_score = models.FloatField(default=0.0)
