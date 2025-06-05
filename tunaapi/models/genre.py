from django.db import models

class Genre(models.Model):
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.description

    class Meta:
        verbose_name = "Genre"
        verbose_name_plural = "Genres"
        ordering = ['description']
